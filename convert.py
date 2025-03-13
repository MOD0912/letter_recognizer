import os
from PIL import Image

def extract_letters(image_path, output_dir):
    
    letter_width = 150
    letter_height = 150
    lst1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    lst2 = ["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    count4 = -8
    for file in os.listdir(image_path):
        print(file)
        if not "copy" in file:
            continue
        image = Image.open(f"pictures/{file}")
        #image = Image.open(f"pictures/1.jpg")
        print("size", image.size)   
        if int(file[0])%2 == 0:
            lst = lst1.copy()
            spacing_x = 40
            spacing_y = 40
            count4+=8
            #continue
            
        else:
            lst = lst2.copy()
            spacing_x = 26
            spacing_y = 27


        width, height = image.size
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        count = 0
        count3 = 0
        
        for j in range(25, height, letter_height+spacing_y):
            count2 = 0
            count3 += 1
            for i in range(15, width, letter_width+spacing_x):
                #print(count3)
                count2 += 1
                if count2 == 9 or count3 >= 14:
                    break
                box = (i, j, i + letter_width, j + letter_height)
                letter_image = image.crop(box)
                count += 1
                letter_image = letter_image.resize((28, 28))
                letter_image = letter_image.convert('L')
                print(count4, count2)
                letter_image.save(os.path.join(output_dir, f'{lst[count3-1]}{count2+count4}.png'))
        

def main():
    pictures_dir = 'pictures'
    output_dir = 'output'
    extract_letters(pictures_dir, output_dir)


'''
delete every file in the output directory
'''
def delete_output():
    output_dir = 'output'
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
                  
if __name__ == "__main__":
    delete_output() 
    main()
