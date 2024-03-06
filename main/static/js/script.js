'use strict';

const { createApp, ref } = Vue;
const { createVuetify } = Vuetify;

const vuetify = createVuetify({
    icons: {
        defaultSet: 'mdi', // This is already the default value - only for display purposes
    },
})


createApp ({
  data() {
    return {
      tab: 'first',
      logregtab: 'log'
    };
  },
}).use(vuetify).mount('body');
