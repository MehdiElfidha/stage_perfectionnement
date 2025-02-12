<template>
  <div>
  <header class="app-header">
    <div class="header-left">
      <div class="logo"><img src="img/logo-sagemcom-new-charte-header.png" alt=""></div>
    </div>
    
    <div class="user-panel">
      <span class="username">{{ currentUser.name || currentUser.email }}</span>
      <button @click="logout" class="logout-btn">
        <i class="fas fa-sign-out-alt"></i>
        Déconnexion
      </button>
    </div>
  </header>

  <div class="admin-container">
    <h2 class="admin-title">Gestion des utilisateurs</h2>

    <!-- Message d'erreur -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    
    <div class="user-form">
      <input v-model="newUser.email" type="email" placeholder="Email" class="form-input">
      <input v-model="newUser.password" type="password" placeholder="Mot de passe" class="form-input">
      <select v-model="newUser.role" class="form-input">
        <option value="user">Utilisateur normal</option>
        <option value="admin">Administrateur</option>
      </select>
      <button @click="addUser" class="auth-btn">Ajouter</button>
    </div>

    <div class="users-list">
      <div v-for="(user, index) in users" :key="index" class="user-card">
        <div class="user-info">
          <span>{{ user.email }}</span>
          <span class="role-badge">{{ user.role }}</span>
        </div>
        <button 
          @click="deleteUser(index)" 
          :disabled="user.email === currentUser.email"
          class="delete-btn">
          Supprimer
        </button>
      </div>
    </div>
  </div>
  </div>
  <footer class="app-footer">
  <div class="footer-content">
    <div class="footer-section">
      <div class="logo-footer">Sagemcom</div>
      <p class="footer-slogan">Solutions innovantes pour la gestion de données</p>
      <div class="social-links">
        <a href="#" class="social-link">
          <i class="fab fa-linkedin"></i>
        </a>
        <a href="#" class="social-link">
          <i class="fab fa-twitter"></i>
        </a>
        <a href="#" class="social-link">
          <i class="fab fa-github"></i>
        </a>
      </div>
    </div>

    <div class="footer-columns">
      <div class="footer-col">
        <h4>Navigation</h4>
        <router-link to="/compare" class="footer-link">Comparateur</router-link>
        <router-link to="/docs" class="footer-link">Documentation</router-link>
        <router-link to="/stats" class="footer-link">Statistiques</router-link>
      </div>

      <div class="footer-col">
        <h4>Légal</h4>
        <a href="#" class="footer-link">Confidentialité</a>
        <a href="#" class="footer-link">CGU</a>
        <a href="#" class="footer-link">Cookies</a>
      </div>

      <div class="footer-col">
        <h4>Contact</h4>
        <a href="mailto:support@sagemcom.com" class="footer-link">support@sagemcom.com</a>
        <a href="tel:+33123456789" class="footer-link">+33 1 23 45 67 89</a>
        <p class="footer-link">Paris, France</p>
      </div>
    </div>
  </div>

  <div class="footer-bottom">
    <p>© 2024 Sagemcom. Tous droits réservés.</p>
    <div class="tech-stack">
      <span>Powered by :</span>
      <i class="fab fa-vuejs"></i>
      <i class="fab fa-python"></i>
      <i class="fas fa-database"></i>
    </div>
  </div>
</footer>
</template>

<script>
import { authService } from '../utils/auth'

export default {
data() {
  return {
    newUser: { email: '', password: '', role: 'user' },
    users: authService.getUsers(),
    errorMessage: '' // Ajout de la variable d'erreur
  }
},
computed: {
  currentUser() {
    return this.$store.state.currentUser || {}
  }
},
methods: {
  logout() {
    this.$store.commit('SET_USER', null)
    this.$router.push('/login')
  },
  addUser() {
    // Réinitialisation des erreurs
    this.errorMessage = ''

    // Vérification des champs requis
    if (!this.newUser.email || !this.newUser.password) {
      this.errorMessage = 'Veuillez remplir tous les champs'
      setTimeout(() => this.errorMessage = '', 3000)
      return
    }

    // Vérification de l'unicité de l'email
    const emailExists = this.users.some(user => 
      user.email.toLowerCase() === this.newUser.email.toLowerCase()
    )

    if (emailExists) {
      this.errorMessage = 'Cet email est déjà utilisé !'
      setTimeout(() => this.errorMessage = '', 3000)
      return
    }

    // Ajout de l'utilisateur si tout est valide
    this.$store.dispatch('addUser', { ...this.newUser })
    this.users = authService.getUsers()
    this.newUser = { email: '', password: '', role: 'user' }
  },
  deleteUser(index) {
    const users = authService.getUsers()
    users.splice(index, 1)
    authService.saveUsers(users)
    this.users = users
  }
}
}
</script>

<style scoped>
.error-message {
padding: 1rem;
margin: 1rem 0;
background: #fef2f2;
color: #dc2626;
border-radius: 8px;
border: 1px solid #fecaca;
animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
from {
  opacity: 0;
  transform: translateY(-20px);
}
to {
  opacity: 1;
  transform: translateY(0);
}
}

/* Le reste du CSS reste inchangé */
.app-header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 1rem 2rem;
background: white;
box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
border-radius: 12px;
margin-bottom: 2rem;
}

.admin-container {
max-width: 800px;
margin: 2rem auto;
padding: 2.5rem;
background: white;
border-radius: 16px;
box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.app-header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 1rem 2rem;
background: white;
box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
border-radius: 12px;
margin-bottom: 2rem;
}

.header-left {
display: flex;
align-items: center;
gap: 2rem;
}

.logo {
font-size: 1.5rem;
font-weight: 700;
color: #2563eb;
}

.nav-links {
display: flex;
gap: 1.5rem;
}

.nav-link {
color: #64748b;
text-decoration: none;
padding: 0.5rem 1rem;
border-radius: 8px;
transition: all 0.3s ease;
}

.nav-link:hover {
background: #f1f5f9;
color: #2563eb;
}

.user-panel {
display: flex;
align-items: center;
gap: 1.5rem;
}

.username {
font-weight: 500;
color: #1e293b;
padding: 0.5rem 1rem;
background: #f8fafc;
border-radius: 8px;
}

.logout-btn {
display: flex;
align-items: center;
gap: 0.5rem;
padding: 0.75rem 1.5rem;
background: #fef2f2;
color: #dc2626;
border: none;
border-radius: 8px;
cursor: pointer;
transition: all 0.3s ease;
font-weight: 500;
}

.logout-btn:hover {
background: #fee2e2;
transform: translateY(-1px);
}

.logout-btn i {
font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
.app-header {
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

.header-left {
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

.user-panel {
  width: 100%;
  justify-content: space-between;
}
}
.admin-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.admin-title {
  text-align: center;
  font-size: 1.8rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.user-form {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.form-input {
  width: 96%;
  padding: 0.9rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  outline: none;
}

.auth-btn {
  width: 100%;
  padding: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.auth-btn:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-1px);
}

.users-list {
  border-top: 2px solid #eee;
  padding-top: 1rem;
}

.user-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin: 0.5rem 0;
  background: #f8fafc;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.role-badge {
  background: #2563eb;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.delete-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}
.app-footer {
background: rgba(255, 255, 255, 0.9);
backdrop-filter: blur(10px);
border-top: 1px solid rgba(37, 99, 235, 0.1);
margin-top: auto;
padding: 2rem 1rem;
box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.03);
}

.footer-content {
max-width: 1200px;
margin: 0 auto;
display: grid;
grid-template-columns: 1fr 2fr;
gap: 3rem;
padding-bottom: 2rem;
}

.logo-footer {
font-size: 1.8rem;
font-weight: 700;
color: #2563eb;
margin-bottom: 1rem;
}

.footer-slogan {
color: #64748b;
margin-bottom: 1.5rem;
line-height: 1.5;
}

.social-links {
display: flex;
gap: 1rem;
}

.social-link {
width: 40px;
height: 40px;
border-radius: 8px;
background: #f1f5f9;
display: flex;
align-items: center;
justify-content: center;
color: #64748b;
transition: all 0.3s ease;
}

.social-link:hover {
background: #2563eb;
color: white;
transform: translateY(-2px);
}

.footer-columns {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 2rem;
}

.footer-col h4 {
color: #1e293b;
margin-bottom: 1.2rem;
font-size: 1.1rem;
}

.footer-link {
display: block;
color: #64748b;
margin-bottom: 0.8rem;
text-decoration: none;
transition: all 0.2s ease;
}

.footer-link:hover {
color: #2563eb;
transform: translateX(5px);
}

.footer-bottom {
max-width: 1200px;
margin: 2rem auto 0;
padding-top: 2rem;
border-top: 1px solid rgba(37, 99, 235, 0.1);
display: flex;
justify-content: space-between;
align-items: center;
color: #64748b;
}

.tech-stack {
display: flex;
align-items: center;
gap: 1.5rem;
}

.tech-stack i {
font-size: 1.5rem;
color: #64748b;
transition: color 0.3s ease;
}

.tech-stack i:hover {
color: #2563eb;
}

@media (max-width: 768px) {
.footer-content {
  grid-template-columns: 1fr;
}

.footer-columns {
  grid-template-columns: 1fr;
}

.footer-bottom {
  flex-direction: column;
  gap: 1rem;
  text-align: center;
}
}

.dark .app-footer {
background: rgba(15, 23, 42, 0.9);
border-top-color: rgba(99, 102, 241, 0.1);
}

.dark .logo-footer,
.dark .footer-col h4 {
color: #e2e8f0;
}

.dark .footer-link,
.dark .footer-slogan,
.dark .tech-stack i,
.dark .footer-bottom {
color: #94a3b8;
}

.dark .social-link {
background: rgba(30, 41, 59, 0.5);
}

.dark .footer-link:hover {
color: #60a5fa;
}
</style>