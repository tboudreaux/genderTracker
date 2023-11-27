import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      currentUser: null,
      isAuthenticated: false,
      isGuest: false,
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
    // other mutations...
  },
  actions: {
    login(context, payload) {
      context.commit('login', payload);
    },
    logout(context){
      context.commit('logout');
    }
    // asynchronous operations...
  },
  // include getters if you have any
});

