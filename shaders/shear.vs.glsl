#version 120
attribute vec2 coord2d;
void pass2(void) {
    vec2 c = mat2(cos(1.0), -sin(0.5),
                  sin(20.0),  cos(1.0)) * coord2d;
    gl_Position = vec4(c, 0.0, 1.0);
}
