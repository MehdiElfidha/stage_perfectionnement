<template>
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

  <div class="main-container">
    <div class="content-container">
      <h2 class="title">Comparaison de fichiers</h2>

      <div class="upload-section">
        <div class="upload-card">
          <h3>Fichier Excel</h3>
          <div class="upload-area" @click="triggerFileInput('excel')">
            <i class="fas fa-file-excel"></i>
            <p>Cliquez pour sélectionner un fichier Excel</p>
            <input type="file" 
                 ref="excelInput" 
                 @change="handleFileUpload($event, 'excel')" 
                 hidden
                 accept=".xls,.xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
          </div>
          <div v-if="files.excel" class="file-info">
            <i class="fas fa-check-circle success-icon"></i>
            <p>{{ files.excel.name }}</p>
          </div>
        </div>

        <div class="compare-button" @click="uploadFiles" :class="{ disabled: !files.excel || !files.log }">
          <i class="fas fa-play"></i>
        </div>

        <div class="upload-card">
          <h3>Fichier Log</h3>
          <div class="upload-area" @click="triggerFileInput('log')">
            <i class="fas fa-file-alt"></i>
            <p>Cliquez pour sélectionner un fichier Log</p>
            <input type="file" 
                 ref="logInput" 
                 @change="handleFileUpload($event, 'log')" 
                 hidden
                 accept=".log,text/plain">
          </div>
          <div v-if="files.log" class="file-info">
            <i class="fas fa-check-circle success-icon"></i>
            <p>{{ files.log.name }}</p>
          </div>
        </div>
      </div>

      <div v-if="results" class="results-section">
        <h3 class="results-title">Résultats de la comparaison</h3>

        <div v-if="results.length > 0">
          <div class="final-result" :class="{ 'conforme': allTestsConform, 'non-conforme': !allTestsConform }">
            <i :class="allTestsConform ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
            {{ allTestsConform ? 'Conforme' : 'Non Conforme' }}
          </div>

          <div v-for="(resultat, index) in results" :key="index" class="test-case">
            <div class="test-header">
              <span class="test-label">Test Excel:</span>
              <span class="test-value">{{ resultat['Test Excel'] }}</span>
              <span class="test-separator">||</span>
              <span class="test-label">Test Log:</span>
              <span class="test-value">{{ resultat['Test Log'] }}</span>
            </div>

            <div class="results-table">
              <table>
                <thead>
                  <tr>
                    <th v-for="(header, idx) in headers" :key="idx">{{ header }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(donnee, idx) in resultat['Données']" :key="idx">
                    <td>{{ donnee['Nom Excel'] }}</td>
                    <td>{{ donnee['Nom Log'] }}</td>
                    <td>{{ formatValue(donnee['Min Excel']) }}</td>
                    <td>{{ formatValue(donnee['Min Log']) }}</td>
                    <td :class="{ 'success-cell': donnee['Min Identique'] }">
                      {{ donnee['Min Identique'] ? '✓' : '✗' }}
                    </td>
                    <td>{{ formatValue(donnee['Max Excel']) }}</td>
                    <td>{{ formatValue(donnee['Max Log']) }}</td>
                    <td :class="{ 'success-cell': donnee['Max Identique'] }">
                      {{ donnee['Max Identique'] ? '✓' : '✗' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-else class="no-results">
          <i class="fas fa-exclamation-triangle"></i>
          Aucun test correspondant trouvé
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
import axios from "axios";

export default {
  data() {
    return {
      files: { excel: null, log: null },
      results: null,
      headers: [
        'Nom Excel', 'Nom Log', 
        'Min Excel', 'Min Log', 'Identique Min',
        'Max Excel', 'Max Log', 'Identique Max'
      ]
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.currentUser || {}
    },
    allTestsConform() {
      if (!this.results || this.results.length === 0) return false;
      return this.results.every(resultat => 
        resultat.Données.every(donnee => 
          donnee['Min Identique'] && donnee['Max Identique']
        )
      );
    }
  },
  methods: {
    logout() {
      this.$store.commit('SET_USER', null)
      this.$router.push('/login')
    },
    triggerFileInput(type) {
      this.$refs[`${type}Input`].click();
    },
    handleFileUpload(event, type) {
      const file = event.target.files[0];
      if (!file) return;

      const validTypes = {
        excel: [
          'application/vnd.ms-excel',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          '.xls',
          '.xlsx'
        ],
        log: [
          'text/plain',
          '.log'
        ]
      };
      const isValid = validTypes[type].some(t => 
        file.type.includes(t) || file.name.toLowerCase().endsWith(t)
      );

      if (!isValid) {
        alert(`Type de fichier invalide pour ${type.toUpperCase()} !`);
        event.target.value = '';
        this.files[type] = null;
        this.results = null;
        return;
      }

      this.files[type] = file;
      this.results = null;
    },
    async uploadFiles() {
      if (!this.files.excel || !this.files.log) return;

      const formData = new FormData();
      formData.append("excel", this.files.excel);
      formData.append("log", this.files.log);

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/compare", formData);
        const sanitizedData = response.data.replace(/NaN/g, 'null');
        this.results = JSON.parse(sanitizedData).results;
      } catch (error) {
        console.error("Erreur:", error);
        alert("Erreur lors de la comparaison");
      }
    },
    formatValue(value) {
      return isNaN(value) || value === null ? "N/A" : value;
    }
  }
};
</script>

<style scoped>
/* Styles existants conservés */
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

/* ... (conserver tous les styles existants) ... */

.final-result {
  padding: 1rem;
  border-radius: 8px;
  margin: 2rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
  font-size: 1.2rem;
  justify-content: center;
  transition: all 0.3s ease;
}

.conforme {
  background: #dcfce7;
  color: #166534;
  border: 2px solid #22c55e;
}

.non-conforme {
  background: #fee2e2;
  color: #991b1b;
  border: 2px solid #ef4444;
}

.final-result i {
  font-size: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .final-result {
    font-size: 1rem;
    padding: 0.8rem;
  }
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
/* Utilisez les styles de la première réponse et ajoutez : */

.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.upload-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin: 40px 0;
}

.upload-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  width: 350px;
  transition: transform 0.3s ease;
}

.upload-card:hover {
  transform: translateY(-5px);
}

.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-area:hover {
  border-color: #3b82f6;
}
.upload-area i {
  font-size: 40px;
  color: #3b82f6;
  margin-bottom: 15px;
}

.compare-button {
  background: #3b82f6;
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.compare-button:hover:not(.disabled) {
  background: #2563eb;
  transform: scale(1.1);
}

.compare-button.disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.results-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-top: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.results-table {
  overflow-x: auto;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background: #f8fafc;
  font-weight: 600;
}

.success-cell {
  color: #10b981;
  font-weight: bold;
}

.test-header {
  background: #f8fafc;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.no-results {
  text-align: center;
  padding: 30px;
  color: #64748b;
}

.file-info {
  margin-top: 15px;
  padding: 10px;
  background: #f8fafc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-info p {
  white-space: nowrap; /* Empêche le texte de se diviser sur plusieurs lignes */
  overflow: hidden; /* Cache tout débordement de texte */
  text-overflow: ellipsis; /* Ajoute "..." lorsque le texte déborde */
  max-width: 100%; /* Assure que le texte n'atteint pas la largeur totale */
  display: block; /* Assure que le texte est sur une seule ligne */
}
.success-icon {
  color: #10b981;
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
  border-radius: 30px;
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
/* Ajoutez les styles du header de la première réponse */
</style>