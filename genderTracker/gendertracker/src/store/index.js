import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state() {
    return {
      currentUser: null,
      isAuthenticated: false,
      isGuest: false,
      genderList: null,
      // other states...
    };
  },
  mutations: {
    login(state, payload) {
      state.isAuthenticated = true;
      state.isGuest = payload.isGuest;
      if (state.isGuest == true) {
        state.currentUser = 'Guest'
      } else {
        state.currentUser = payload.user;
      }

    },
    logout(state) {
      state.isAuthenticated = false;
      state.isGuest = false;
      state.currentUser = null;
    },
    setGenderList(state, payload) {
      state.genderList = payload;
    }
    // other mutations...
  },
  actions: {
    login(context, payload) {
      context.commit('login', payload);
    },
    logout(context){
      context.commit('logout');
    },
    setGenderList(context) {
      axios
        .get('/api/gender/list')
        .then((response) => {
          context.commit('setGenderList', response.data)
        })
        .catch((error) => {
          console.log(error);
        });
    }
    // asynchronous operations...
  },
  // include getters if you have any
});

