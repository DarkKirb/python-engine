#version 120
varying vec2 f_texture_uv;
uniform sampler2D texture_tileset;

void main(void) {
    gl_FragColor = texture2D(texture_tileset, f_texture_uv);
}
