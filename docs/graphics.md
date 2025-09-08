# Graphics & Visualization in TechLang

TechLang provides commands for creating graphics, drawing shapes, and visualizing data.

## Drawing Shapes

Draw a window and basic shapes:

```techlang
window("My Drawing", 400, 300)
rect(50, 50, 100, 80, color="blue")
circle(200, 150, 40, color="red")
line(10, 10, 390, 290, color="green")
```

## Working with Images

Load and display an image:

```techlang
img = load_image("picture.png")
draw_image(img, 100, 100)
```

Save the current canvas to a file:

```techlang
save_canvas("output.png")
```

## Data Visualization

Plot a simple chart:

```techlang
plot([1, 3, 2, 5, 4], title="Sample Plot")
```

Create a bar chart:

```techlang
bar_chart(["A", "B", "C"], [5, 2, 7], title="Bar Chart")
```

---

See the [Examples Index](examples.md) for