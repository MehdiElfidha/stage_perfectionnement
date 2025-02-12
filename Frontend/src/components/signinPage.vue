<template>
  <div class="main-container">
    <transition name="slide">
      <div v-if="errorMessage" class="error-banner">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>
    </transition>

    <div class="auth-wrapper">
      <div class="auth-card">
        <div class="card-header">
          <i class="fas fa-user-plus auth-icon"></i>
          <h2 class="auth-title">Créer un compte</h2>
        </div>

        <form @submit.prevent="handleSubmit" class="auth-form">
          <div class="input-group">
            <label class="input-label">
              <i class="fas fa-user input-icon"></i>
              <input
                type="text"
                v-model="form.name"
                placeholder="Nom complet"
                class="form-input"
                required
              />
            </label>
          </div>

          <div class="input-group">
            <label class="input-label">
              <i class="fas fa-envelope input-icon"></i>
              <input
                type="email"
                v-model="form.email"
                placeholder="Adresse email"
                class="form-input"
                required
              />
            </label>
          </div>

          <div class="input-group">
            <label class="input-label">
              <i class="fas fa-lock input-icon"></i>
              <input
                type="password"
                v-model="form.password"
                placeholder="Mot de passe"
                class="form-input"
                required
              />
            </label>
          </div>

          <button type="submit" class="auth-btn" :disabled="loading">
            <span v-if="!loading">Créer un compte</span>
            <i v-else class="fas fa-spinner fa-spin"></i>
          </button>

          <div class="auth-links">
            <span>Déjà un compte ?</span>
            <router-link to="/login" class="text-link">Se connecter</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: ''
      },
      loading: false,
      errorMessage: null,
      timeoutId: null
    };
  },
  methods: {
    async handleSubmit() {
      try {
        this.loading = true;
        
        await this.$store.dispatch('addUser', {
          ...this.form,
          role: 'user',
          createdAt: new Date()
        });

        this.$router.push('/login');
        this.form = { name: '', email: '', password: '' };

      } catch (error) {
        this.showError(`Erreur: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    showError(message) {
      this.errorMessage = message;
      if (this.timeoutId) clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessage = null;
      }, 3000);
    }
  },
  beforeUnmount() {
    if (this.timeoutId) clearTimeout(this.timeoutId);
  }
};
</script>

<style scoped>
.error-banner {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #f8d7da;
  color: #721c24;
  padding: 1rem 2rem;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-banner i {
  font-size: 1.2rem;
}

.slide-enter-active {
  animation: slide-in 0.3s;
}

.slide-leave-active {
  animation: slide-out 0.3s;
}

@keyframes slide-in {
  from {
    top: -100px;
    opacity: 0;
  }
  to {
    top: 20px;
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    top: 20px;
    opacity: 1;
  }
  to {
    top: -100px;
    opacity: 0;
  }
}

/* Conserver les styles existants ci-dessous */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 2rem;
  background: transparent;
}

.auth-card {
  background: whtite;
  width: 100%;
  max-width: 440px;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  transform: translateY(0);
  transition: all 0.3s ease;
}

/* ... (conserver tous les autres styles existants) ... */
  /* Utiliser les mêmes styles que la page de login */
  .auth-card {
    max-width: 480px;
  }
  
  .input-group {
    margin-bottom: 1.2rem;
  }
  
  .form-input {
    padding: 0.9rem 1rem 0.9rem 2.8rem;
  }
  
  .auth-links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
    color: #64748b;
  }
  
  /* Ajouts spécifiques à la page d'inscription */
  .password-rules {
    margin: 0.5rem 0;
    padding: 0.8rem;
    background: #f8fafc;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #64748b;
  }
  
  .password-rules ul {
    list-style: none;
    padding-left: 0;
    margin: 0.5rem 0;
  }
  
  .password-rules li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.3rem 0;
  }
  
  .password-rules i {
    color: #2563eb;
    font-size: 0.8rem;
  }
  
  .terms-text {
    font-size: 0.9rem;
    color: #64748b;
    text-align: center;
    margin: 1rem 0;
  }
  
  .terms-link {
    color: #2563eb;
    text-decoration: none;
  }
  
  .terms-link:hover {
    text-decoration: underline;
  }
  
  @media (max-width: 480px) {
    .auth-card {
      padding: 1.5rem;
    }
    
    .auth-title {
      font-size: 1.5rem;
    }
  }
  .auth-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 80px);
    padding: 2rem;
    background: transparent;
  }
  
  .auth-card {
    background: white;
    width: 100%;
    max-width: 440px;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transform: translateY(0);
    transition: all 0.3s ease;
  }
  
  .auth-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.1);
  }
  
  .card-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .auth-icon {
    font-size: 2.5rem;
    color: #2563eb;
    margin-bottom: 1rem;
  }
  
  .auth-title {
    font-size: 1.8rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
  
  .input-group {
    margin-bottom: 1.5rem;
  }
  
  .input-label {
    position: relative;
    display: block;
  }
  
  .input-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #64748b;
    font-size: 1.1rem;
  }
  
  .form-input {
    width: 85%;
    padding: 0.9rem 1rem 0.9rem 2.8rem;
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
  
  .auth-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  .divider {
    display: flex;
    align-items: center;
    margin: 2rem 0;
  }
  
  .divider-line {
    flex: 1;
    height: 1px;
    background: #e2e8f0;
  }
  
  .divider-text {
    padding: 0 1rem;
    color: #64748b;
    font-size: 0.9rem;
  }
  
  .social-auth {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .social-btn {
    width: 48px;
    height: 48px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .social-btn:hover {
    border-color: #2563eb;
    transform: translateY(-2px);
  }
  
  .social-btn.google:hover {
    color: #DB4437;
    border-color: #DB4437;
  }
  
  .social-btn.microsoft:hover {
    color: #00A4EF;
    border-color: #00A4EF;
  }
  
  .auth-links {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
  }
  
  .text-link {
    color: #2563eb;
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s ease;
  }
  
  .text-link:hover {
    color: #1d4ed8;
    text-decoration: underline;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .auth-card {
      padding: 1.5rem;
    }
    
    .auth-links {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    
    .header {
      padding: 1rem;
    }
    
    .nav-links {
      display: none;
    }
  }
  </style>