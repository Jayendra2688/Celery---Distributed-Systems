from PIL import Image
from celery import shared_task
from celery_app import app
from celery import current_task
import os
import time
@app.task
def compute_the_part_of_fractal(width,height,x_min,x_max,y_min,y_max,used_color,filename):
    start_time = time.perf_counter()
    worker_name = current_task.request.hostname  
    max_iter = 200  
    # Create image
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    for px in range(width):
        for py in range(height):
            # Map pixel position to complex plane
            x0 = x_min + (px / (width-1)) * (x_max - x_min)
            y0 = y_min + (py / (height-1)) * (y_max - y_min)
            c = complex(x0, y0)
            z = 0 + 0j
            iteration = 0
            while abs(z) <= 2 and iteration < max_iter:
                z = z*z + c
                iteration += 1

            # Color mapping
            color = 255 - int(iteration * 255 / max_iter)
            rgb = tuple(int(used_color[i:i+2], 16) for i in (0, 2, 4))
            if color!=0:
                pixels[px, py] = rgb
            else:
                pixels[px,py] = (0,0,0)

    # Save image
    img.save(filename)
    end_time = time.perf_counter()
    return filename,worker_name.split('@')[0],end_time-start_time

@app.task
def combine_fractals(results,width,height,filename): 
    final_results = []
    start_time = time.perf_counter()
    final_image = Image.new("RGB",(width,height))
    results =sorted(results, key=lambda x: x[0][-1])
    for i in range(len(results)):
        img = Image.open(results[i][0])
        final_image.paste(img,(i*100,0))
    final_image.save(filename)
    end_time = time.perf_counter()
    max_worker_time = max(result[2] for result in results)
    for i in range(len(results)):
        text = f"{results[i][0]} created by {results[i][1]} -> {results[i][2]:.4f} secs"
        final_results.append(text)
    combine_fractal_time = end_time - start_time 
    final_results.append(f"{filename} created, for combining ->  {combine_fractal_time:.4f} secs")
    final_results.append(f"{filename} created, total time taken -> {max_worker_time + combine_fractal_time:.4f} secs")
    return filename,final_results

@app.task
def add(x, y):
    start_time = time.perf_counter()
    time.sleep(2)
    worker_name = current_task.request.hostname  # e.g., 'celery@worker1'
    pid = os.getpid()  # process ID
    print(f"Task add({x},{y}) running on {worker_name}, PID={pid}")
    end_time = time.perf_counter()
    msg = f"Add({x},{y}) took {end_time - start_time :.4f} secs on {worker_name.split('@')[0]}"
    return x + y,msg