from celery import chord
from tasks import compute_the_part_of_fractal,combine_fractals

if __name__ == "__main__":
    width = 400
    height = 400
    x_min = -1.5 
    x_max = 0.5
    y_min = -1
    y_max = 1
    colors = ['84994F','FFE797','FCB53B','B45253']
    
    result = chord(
    [
        compute_the_part_of_fractal.s(width//4,height,-1.5,-1,-1,1,colors[0],"generated_images/image_set1.png"),
        compute_the_part_of_fractal.s(width//4,height,-1,-0.5,-1,1,colors[1],"generated_images/image_set2.png"),
        compute_the_part_of_fractal.s(width//4,height,-0.5,0,-1,1,colors[2],"generated_images/image_set3.png"),
        compute_the_part_of_fractal.s(width//4,height,0,0.5,-1,1,colors[3],"generated_images/image_set4.png"),
    ],
    combine_fractals.s(width,height,"generated_images/mandelbrot_combined.png")
    )()
    
    filename,final_res = result.get()
    
    for i in range(len(final_res)):
        print(f'{final_res[i]}')