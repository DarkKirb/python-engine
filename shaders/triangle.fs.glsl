#version 120
varying vec2 f_texcoord;
uniform float fade;
uniform sampler2D texture_box;
void main(void) {
    vec4 c = texture2D(texture_box, f_texcoord);
    c.a = fade;
    gl_FragColor = c;
}

