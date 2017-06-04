#version 120
//Input
attribute vec2 coord2d;
attribute vec2 texture_uv;
//Output
varying vec2 f_texture_uv;

//Constants
uniform float xScroll;
uniform float yScroll;
uniform float xRot;
uniform float yRot;
uniform float zRot;
uniform float zoom;
uniform mat4 aspectRatio;
vec4 rotateX(vec4 pos) {
    float a=xRot;
    mat4 m = mat4(1.0, 0.0,    0.0,     0.0,
                  0.0, cos(a), -sin(a), 0.0,
                  0.0, sin(a), cos(a),  0.0,
                  0.0, 0.0,    0.0,     1.0);
    return m * pos;
}
vec4 rotateY(vec4 pos) {
    float a=yRot;
    mat4 m = mat4(cos(a),  0.0, sin(a), 0.0,
                  0.0,     1.0, 0.0,    0.0,
                  -sin(a), 0.0, cos(a), 0.0,
                  0.0,     0.0, 0.0,    1.0);
    return m * pos;
}
vec4 rotateZ(vec4 pos) {
    float a=zRot;
    mat4 m = mat4(cos(a), -sin(a), 0.0, 0.0,
                  sin(a),  cos(a), 0.0, 0.0,
                  0.0,     0.0,    1.0, 0.0,
                  0.0,     0.0,    0.0, 1.0);
    return m * pos;
}
void main(void) {
    vec4 pos = vec4(coord2d, 0.0, 1.0);
    gl_Position = aspectRatio * pos;
    //Apply scroll
    pos = vec4(pos.x + xScroll, pos.y + yScroll, 0.0, 1.0);
    //Apply rotations
    pos = rotateX(rotateY(rotateZ(pos)));
    //Finally, zooming and aspect ratio correction
    gl_Position = aspectRatio * vec4(pos.xyz, zoom);
    gl_Position = gl_Position;
    //Set the varying
    f_texture_uv = texture_uv;
}
