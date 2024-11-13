// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCXjqn0cYc-EJXHNo6Q66uyOzFoXB2TECw",
  authDomain: "chatterbox-ea63f.firebaseapp.com",
  projectId: "chatterbox-ea63f",
  storageBucket: "chatterbox-ea63f.firebasestorage.app",
  messagingSenderId: "950634131284",
  appId: "1:950634131284:web:e6b192a22bd59154dca2c1",
  measurementId: "G-FLQQ935VB7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
