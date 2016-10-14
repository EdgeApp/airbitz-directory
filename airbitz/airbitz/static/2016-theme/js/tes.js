/*
 * Basic Overview:
 * Generate a mesh of triangles that share the same points so that the mesh
 * is, well, a mesh.
 * Jitter the x and y positions of the points to simulate random movement
 * of waves.
 * Move the y position of the points at certain times to simulate larger
 * wave movements.
 */
function Waves(options) {

    this.x         = options.x         || 0;
    this.y         = options.y         || 0;
    this.width     = options.width     || 800;
    this.height    = options.height    || 800;
    this.container = document.getElementById('canvas-container');

    this.diagonal = Math.sqrt(this.width * this.width +
                              this.height * this.height);

    this.renderer = PIXI.autoDetectRenderer(this.width, this.height);
    this.resizeCanvas();
    this.container.appendChild(this.renderer.view);
    requestAnimationFrame(this.draw.bind(this));

}

/*
 * Loop through all the triangles, tell them the new global time, and
 * render.
 */
Waves.prototype.draw = function(time) {
    for(var i = 0, len = this.vectors.length; i < len; i++) {
        this.vectors[i].update(time);
    }
    this.graphics.clear();
    for(var i = 0, len = this.triangles.length; i < len; i++) {
        this.triangles[i].draw();
    }
    this.renderer.render(this.stage);
    requestAnimationFrame(this.draw.bind(this));
}

/**
 * GenerateTriangles creates triangles by traversing a grid and adding
 * two triangles for each square.
 */
Waves.prototype.generateTriangles = function() {
    var originX = this.x - 150
        , originY = this.y - 150
        , width   = this.width + 300
        , height  = this.height + 300
        , deltaX  = 80
        , deltaY  = 30
        , columns = Math.ceil(width / deltaX)
        , rows    = Math.ceil(height / deltaY)
        , v0, v1, v2;

    var triangles = this.triangles = new Array(2 * rows * columns);
    var vectors   = this.vectors   = new Array((rows + 1) * (columns + 1));
    this.stage    = new PIXI.Stage(0xFFFFFF);
    this.graphics = new PIXI.Graphics();
    this.stage.addChild(this.graphics);

    // This loops through the grid of triangles, all the if statements are for
    // literal corner cases where you need to generate a new point instead of
    // grabbing a point from the adjacent triangle, which is done for
    // optimization and because the waves need to match up in height, which is
    // done easily because they are in fact the same point.
    for(var i = 0; i < rows; i++) {
        if(i % 2 == 1) {
            v1 = vectors[(i + 1) * (columns + 1)] = new Waves.Vector({
                x: originX,
                y: originY + i * deltaY
            });
            v2 = vectors[i * (columns + 1)];
        } else {
            if(i == 0) {
                v1 = vectors[0] = new Waves.Vector({
                    x: originX, y: originY
                });
            } else {
                v1 = vectors[i * (columns + 1)];
            }
            v2 = vectors[(i + 1) * (columns + 1)] = new Waves.Vector({
                x: originX + 0.5 * deltaX,
                y: originY + i * deltaY
            });
        }
        for(var j = 0; j < 2 * columns; j++) {
            v0 = v1;
            v1 = v2;
            if((i + j) % 2 == 1 || i === 0) {
                var row = (i + (i + j) % 2) * (columns + 1);
                v2 = vectors[row + (j >> 1) + 1] = new Waves.Vector({
                    x: v0.x + deltaX,
                    y: v0.y
                });
            } else {
                v2 = vectors[i * (columns + 1) + (j >> 1) + 1];
            }
            triangles[i * columns * 2 + j] = new Waves.Triangle({
                v0: v0, v1: v1, v2: v2,
                graphics: this.graphics,
                waves: this
            });
        }
    }
}

/*
 * Resizes the canvas with respect to the device resolution.
 */
Waves.prototype.resizeCanvas = function() {
    var canvas = this.renderer.view
        , height = this.height
        , width  = this.width
        , ratio  = window.devicePixelRatio || 1;
    this.renderer.resize(width * ratio, height * ratio);
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    this.generateTriangles();
}

/*
 * http://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
 */
Waves.hslToRgb = function(h, s, l){
    var r, g, b;
    if(s == 0) {
        r = g = b = l;
    } else{
        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = Waves.hue2rgb(p, q, h + 1/3);
        g = Waves.hue2rgb(p, q, h);
        b = Waves.hue2rgb(p, q, h - 1/3);
    }
    return ((r * 255) << 16) + ((g * 255) << 8) + (b * 255);
}

/*
 * Helper function for 'hslToRgb'.
 */
Waves.hue2rgb = function(p, q, t){
    if(t < 0) t += 1;
    if(t > 1) t -= 1;
    if(t < 1/6) return p + (q - p) * 6 * t;
    if(t < 1/2) return q;
    if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;
}

Waves.Vector = function(options) {
    this.originX = this.x = options.x || 0;
    this.originY = this.y = options.y || 0;
    this.deltaX = this.newDeltaX();
    this.deltaY = this.newDeltaY();
    this.duration = this.newDuration();
    this.start = Date.now() - this.newDuration();
}

Waves.Vector.prototype.update = function(time) {
    // This calculates the vertical difference of a point due to the wave.
    // This works by generating a function that moves a positive slope line
    // from the upper left to the bottom right. The magntitude of the
    // difference is defined by the distance from the point to the line.
    var distance = Math.sin(
            Math.min(
            Math.abs(
                this.originY +
                0.5 * this.originX + 150 -
                time / 5 %
                (
                    Math.max(window.innerWidth, window.innerHeight)
                    + 300
                )
            ) / Math.sqrt(1.25)
                , 200) / 200 * Math.PI / 2
        ) * 60;
    // If the last animation is complete, create a new one.
    if(time > this.start + this.duration) {
        this.start = time;
        this.duration = this.newDuration();
        this.deltaX = this.newDeltaX();
        this.deltaY = this.newDeltaY();
    }
    var delta = (time - this.start) / this.duration
        , sin   = Math.sin(delta * Math.PI * 2);
    this.x = Math.round(this.originX + sin * this.deltaX);
    this.y = Math.round(this.originY + sin * this.deltaY + distance);
}

/*
 * Used to create a random duration for an animation of a point.
 */
Waves.Vector.prototype.newDuration = function() {
    return Math.random() * 1000 + 2000;
}

/*
 * Used to create a random difference in the x position of a point for an
 * animation.
 */
Waves.Vector.prototype.newDeltaX = function() {
    return Math.random() * 20 - 10
}
Waves.Vector.prototype.newDeltaY = function() {
    return Math.random() * 26 - 13;
}

Waves.Triangle = function(options) {
    this.v0 = options.v0;
    this.v1 = options.v1;
    this.v2 = options.v2;
    this.graphics = options.graphics;
    this.waves = options.waves;
    var sumX = this.v0.originX + this.v1.originX + this.v2.originX
        , sumY = this.v0.originY + this.v1.originY + this.v2.originY;
    // Cache the centroid for use in the 'color' function.
    this.centroid = new Waves.Vector({ x: sumX / 3, y: sumY / 3 });
}

Waves.Triangle.prototype.draw = function() {
    var graphics = this.graphics
        , ratio    = window.devicePixelRatio || 1;
    graphics.beginFill(this.color());
    graphics.moveTo(this.v0.x * ratio, this.v0.y * ratio);
    graphics.lineTo(this.v1.x * ratio, this.v1.y * ratio);
    graphics.lineTo(this.v2.x * ratio, this.v2.y * ratio);
    graphics.endFill();
}

/*
 * Computes the area of the triangle from its vertices.
 */
Waves.Triangle.prototype.area = function() {
    return Math.abs(
        (this.v0.x * this.v1.y - this.v1.x * this.v0.y +
         this.v1.x * this.v2.y - this.v2.x * this.v1.y +
         this.v2.x * this.v0.y - this.v0.x * this.v2.y) / 2);
}

/*
 * The hue is determined by the triangle's position on the screen, upper
 * left being darker than the bottom right. The lightness and saturation are
 * based off the area of the triangle. The lightness is defined with an
 * exponential function to imitate a specular reflection as the wave peaks,
 * when the area is largest.
 */
Waves.Triangle.prototype.color = function() {
    var hue = 180, saturation = 0.5, lightness = 0.5;
    var hue = 240 - (Math.abs(0.5 * this.centroid.x + this.centroid.y) /
                     Math.sqrt(1.25) / this.waves.diagonal) * 80
        , area = this.area()
        , saturation = 0.6 + 0.02 * area / 500
        , lightness = Math.min(1, saturation +
                                  0.1 * Math.pow(area / 2500, 10));
    return Waves.hslToRgb(hue / 360, saturation, lightness);
}

window.addEventListener("DOMContentLoaded", function() {
    var waves = new Waves({
        width:  window.innerWidth,
        height: window.innerHeight
    });
    window.addEventListener("resize", function() {
        waves.width  = window.innerWidth;
        waves.height = window.innerHeight;
        waves.diagonal = Math.sqrt(waves.width * waves.width +
                                   waves.height * waves.height);
        waves.resizeCanvas();
    });
});
