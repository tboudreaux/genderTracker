import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import './assets/styles.css';
import Cookies from 'js-cookie';
import axios from 'axios';

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
      store.dispatch('login', {'isGuest': false, 'user': user});
      console.log("Logged in as " + user);
    })
  .catch((error) => {
      console.log("Token validation failed ", error);
    });
}
app.use(store);
app.mount('#app');
