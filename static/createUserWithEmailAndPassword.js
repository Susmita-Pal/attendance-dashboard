import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

var email=document.getElementById('email');
var password=document.getElementById('password');
console.log(email,password);

function f() {
const auth = getAuth();
signInWithEmailAndPassword(auth,email,password)
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed in
    const user = userCredential.user;
    console.log(user)
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    console.log(errorMessage)
  });
console.log("i'm in createUser.js")
}