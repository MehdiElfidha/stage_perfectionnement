import { createStore } from 'vuex'
import { authService } from '../utils/auth'

export default createStore({
  state: {
    currentUser: null
  },
  mutations: {
    SET_USER(state, user) {
      state.currentUser = user
    },
    ADD_USER(state, user) {
      const users = authService.getUsers()
      users.push(user)
      authService.saveUsers(users)
    }
  },
  actions: {
    async login({ commit }, credentials) {
      const users = authService.getUsers()
      const user = users.find(u => 
        u.email.toLowerCase() === credentials.email.toLowerCase().trim() &&
        u.password === credentials.password
      )
      
      if (!user) throw new Error('Identifiants incorrects')
      commit('SET_USER', user)
      return user
    },

    async addUser({ commit }, newUser) {
      const users = authService.getUsers()
      
      if (users.some(u => u.email.toLowerCase() === newUser.email.toLowerCase())) {
        throw new Error('Cet email est déjà utilisé')
      }

      const fullUser = {
        ...newUser,
        createdAt: new Date()
      }
      
      commit('ADD_USER', fullUser)
      return fullUser
    }
  }
})