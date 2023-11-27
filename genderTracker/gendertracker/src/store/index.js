import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      isAuthenticated: false,
      isGuest: false,
      // other states...
    };
  },
  mutations: {
    login(state, payload) {
      state.isAuthenticated = true;
      state.isGuest = payload.isGuest;
    },
    logout(state) {
      state.isAuthenticated = false;
      state.isGuest = false;
    },
    // other mutations...
  },
  actions: {
    // asynchronous operations...
  },
  // include getters if you have any
});

