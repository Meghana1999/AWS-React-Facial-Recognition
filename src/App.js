import { useState } from 'react';
import './App.css';
const uuid = require('uuid');

function App() {
  const [image, setImage] = useState('');
  const [uploadResultMessage, setUploadResultMessage] = useState('Please upload an image to Authenticate');
  const [visitorName, setVisitorName] = useState('placeholder.jpeg');
  const [isAuth, setAuth] = useState(false);

  function sendImage(e){
    e.preventDefault();
    setVisitorName(image.name);
    const visitorImageName = uuid.v4();
    // We are going to call our API Gateway to upload our visitor image to S3 just for records
    // For calling APIs in react , We use Axios typically
    // But we use fetch for this project, bcz its built-in ,  so that we dont have to add external libraries
    // Going to give url/{bucket}/{filename}=> we craeted in API Gateway
    fetch(`https://62iyhku5uj.execute-api.us-east-1.amazonaws.com/dev/myapp-visitor-images/${visitorImageName}.jpeg`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'image/jpeg',
      },
      body: image
    }).then(async () => {
      // Async call, after we upload we are going to call authentication API to check if our vistor is in employee database
      const response = await authenticate(visitorImageName);
      if(response.Message === 'Success'){
        setAuth(true)
        setUploadResultMessage(`Hii ${response['firstName']} ${response['lastName']}, Welcome to Work. Have a Great Productive Day!!!`);
      }
      else{
        setAuth(false)
        setUploadResultMessage('Authentication Failed : This person is not an Employeee!!!')
      }
    }).catch(error=>{
      setAuth(false);
      setUploadResultMessage('There is an Error during Authentication Process. Please Try again')
      console.error(error);
    })
  }

  async function authenticate(visitorImageName){
    const requestUrl = 'https://62iyhku5uj.execute-api.us-east-1.amazonaws.com/dev/employee?' + new URLSearchParams({
      objectKey: `${visitorImageName}.jpeg`
    });
    return await fetch(requestUrl, {
      method:'GET',
      headers:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
      //,
      //mode:'no-cors'
    }).then(response => response.json()) 
    .then((data)=>{
      return data;
    }).catch(error => console.error(error));

  }
// After we take the image of the visitor, we wills end it to the lambda function to authenticate
  return (
    <div className="App">  
         <h2> Meghana's Facial Recognition System</h2>
         
         <form onSubmit={sendImage}> 
         <input type='file' name='image' onChange={e=> setImage(e.target.files[0])}/>
         <button type='submit'> Authenticate</button>
         </form>
         <div className={isAuth ? 'success' : 'failure' }>{uploadResultMessage}</div>
         <img src={ require(`./visitors/${visitorName}`)} alt="Visitor" height={250} width={250}/>

    </div>
  );
}

export default App;
