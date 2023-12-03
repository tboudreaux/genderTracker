import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import './assets/styles.css';
import Cookies from 'js-cookie';
import axios from 'axios';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faGear } from '@fortawesome/free-solid-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faGear);
library.add(faGithub)



const app = createApp(App);
const token = Cookies.get('gt_login_token');

if (token){
  axios
    .get('/login/test', {
    headers: {
      'x-access-tokens': token,
    }
  })
  .then((response) => {
      const user = response.data.username
      console.log(response.data);
      store.dispatch('login', {'isGuest': false, 'user': user, 'public': response.data['username']});
      console.log("Logged in as " + user);
    })
  .catch((error) => {
      console.log("Token validation failed ", error);
    });
}

store.dispatch('setGenderList');

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(store);
app.mount('#app');
