const usersKey = 'fileCompareUsers'

export const authService = {
  getUsers() {
    return JSON.parse(localStorage.getItem(usersKey)) || []
  },

  saveUsers(users) {
    localStorage.setItem(usersKey, JSON.stringify(users))
  },

  initDefaultAdmin() {
    const users = this.getUsers()
    if (!users.some(u => u.role === 'admin')) {
      users.push({
        name: 'Admin',
        email: 'admin@filecompare.com',
        password: 'admin123',
        role: 'admin',
        createdAt: new Date()
      })
      this.saveUsers(users)
    }
  }
}

authService.initDefaultAdmin()