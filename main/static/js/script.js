'use strict';

const { createApp, ref } = Vue;
const { createVuetify } = Vuetify;

const vuetify = createVuetify({
    icons: {
        defaultSet: 'mdi', // This is already the default value - only for display purposes
    },
})

function resizeWindow() {
  let scrollers = document.querySelectorAll(".v-virtual-scroll.pretty_scroll");
  scrollers.forEach((scroll) => {
    scroll.style.height = `${window.innerHeight - 100}px`;
  });
}

let body = document.querySelector("body");
body.addEventListener("mousemove", (event) => {
  resizeWindow();
});

window.onresize = resizeWindow;

createApp ({
  data() {
    return {
      tab: 'first',
      logregtab: 'log'
    };
  },
}).use(vuetify).mount('body');
