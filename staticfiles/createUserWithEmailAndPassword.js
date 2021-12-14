import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

var firebaseConfig={
    apiKey: "AIzaSyBexJb_2s5P3z96b75fU2jhZA8MQAMyuHQ",
  authDomain: "mukhamapp.firebaseapp.com",
  databaseURL: "https://mukhamapp-default-rtdb.firebaseio.com",
  projectId: "mukhamapp",
  storageBucket: "mukhamapp.appspot.com",
  messagingSenderId: "1017209631493",
  appId: "1:1017209631493:web:3ac83a83fc41438d05fd6c",
  measurementId: "G-T1C68K1DBQ"
};

const firebase=initializeApp(firebaseConfig);
const auth=firebase.auth();
document.getElementById('sign_in_submit').addEventListener("click",sign_in)
document.getElementById('sign_up_submit').addEventListener("click",sign_up)

function sign_in() {
    var email=document.getElementById('email');
    var password=document.getElementById('password');
    const promise=auth.signInWithEmailAndPassword(email.value,password.value);
    promise.catch(e=>alert(e.message));
    alert("Sign In");
}

function sign_up() {
    var email=document.getElementById('email');
    var password=document.getElementById('pwd');
    const promise=auth.createUserWithEmailAndPassword(email.value,password.value);
    promise.catch(e=>alert(e.message));
    alert("Signed Up");
}