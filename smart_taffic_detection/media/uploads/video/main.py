from myshape import Shape

def main():
    print("What do you want?")
    print("circle type c")
    print("rectangle type r")
    print("triangle type t")
    ip = input()
    print("type x")
    x = int(input())
    print("type y")
    y = int(input())
    if ip =="c":
        print("input radius")
        radius = input()
        print("input colour")
        col = input()
        Shape.Circle.draw_circle(x,y,int(radius),str(col))
    elif ip =="r":
        print("input side1")
        side1 = input()
        print("input side2")
        side2 = input()
        print("input colour")
        col = input()
        Shape.Rectangle.draw_rectangle(x,y,int(side1),int(side2),col)
    elif ip =="t":
        print("input side")
        side = input()
        print("input colour")
        col = input()
        Shape.Triangle.draw_triangle(x,y,int(side),col)

main()