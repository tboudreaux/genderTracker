import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state() {
    return {
      currentUser: null,
      currentUserPublic: null,
      isAuthenticated: false,
      submissions: 0,
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
        state.currentUser = 'Guest';
        state.currentUserPublic = "Guest";
      } else {
        state.currentUser = payload.user;
        state.currentUserPublic = payload.public;
      }

    },
    logout(state) {
      state.isAuthenticated = false;
      state.isGuest = false;
      state.currentUser = null;
      state.currentUserPublic = null;
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

