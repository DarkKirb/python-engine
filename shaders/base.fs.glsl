#version 120
varying vec2 f_texcoord;
uniform sampler2D texture_box;
void main(void) {
    gl_FragColor = texture2D(texture_box, f_texcoord);
}

