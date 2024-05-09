
import './App.css';
import "bootstrap"
import { useState, useEffect } from "react"
import axios from "axios";
import Swal from "sweetalert2";


function App() {
  const [ipAddress, setIpAddress] = useState();
  const [encryptedIpAddress, setEncryptedIpAddress] = useState();

  const [grantAccess, setGrantAccess] = useState();
  const [message, setMessage] = useState('');




  function isValidIP(ip) {
    var ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
  }

  const handdleEncrypt = async (e) => {
    e.preventDefault();
    if (!isValidIP(ipAddress)) {
      setMessage("Invalid IP address");
      console.log(ipAddress)
      return;
    }
    console.log(ipAddress)
    try {
      const response = await axios.post(`http://127.0.0.1:8000/encrypt_ip/${ipAddress}`)
      console.log(response)
      if (response.data.message === "IP encrypted and stored successfully") {

        const DESPoint = response.data.DESPoint.data.data[0].DESPoint;
        Swal.fire("IP Address is encrypted", "Your IP Address is encrypted successfully", "success");

        console.log(response.data.DESPoint.data.data[0].DESPoint)
        setEncryptedIpAddress(DESPoint)
      } else if (response.data.message === "IP address already exists in the database") {
        setMessage(" This IP ADDRESS already registered & Encrypted ")
        Swal.fire("IP Address is registered", "This IP ADDRESS already registered & Encrypted , Try another IP Address", "Info");
      }
    } catch (e) {
      console.log(e)
    }
  }

  const handdleGrantAccess = async (e) => {
    e.preventDefault();
    if (!grantAccess) {
      setMessage("Invalid Access Code");
      return;
    }
    try {

      const response = await axios.get(`http://127.0.0.1:8000/findDesPoint/${grantAccess}`)
      console.log(response)

      if (response.data.message === "Access Granted successfully") {
        Swal.fire("Access Granted", "Your Encrypted IP address is vaild", "success");
      } else if(response.data.message === "Invalid Access Code ! Please try again") {
        setMessage("Invalid Access Code ! Please try again")
        Swal.fire("Invalid Access Code", "Invalid Access Code! Please try again", "error");
      }
    } catch (error) {
      console.log(error)
    }
  }



  return (
    <div className="App">
      <header className="App-header">
        <div className="form">
          <div className="container">
            {message && <div className='danger'>{message}</div>}
            <EncryptForm ipAddress={ipAddress} setIpAddress={setIpAddress} onSumbit={handdleEncrypt} />
            {encryptedIpAddress && <FeedbackBox encryptedIpAddress={encryptedIpAddress} />}
            <Divder />
            <GrantAccess grantAccess={grantAccess} setGrantAccess={setGrantAccess} onSumbit={handdleGrantAccess} />
          </div>
        </div>
      </header>
    </div>
  );
}


const EncryptForm = (props) => {
  const { ipAddress, setIpAddress, onSumbit } = props;

  const handelChange = (event) => {
    console.log(event.target.value);
    setIpAddress(event.target.value);
  }
  return (
    <div className="row">
      <div className="col-12">
        <h3 className="mt-3">Encrypt your IP Address</h3>
        <form onSubmit={onSumbit}>
          <div className="form-group">
            <label>Enter your IP Address</label>

            <input className="input-ip" type="text" placeholder="Enter your IP Address" onChange={handelChange} />
            <button className="btn-encrypt" type="submit" >Encrypt</button>
          </div>
        </form>

      </div>
    </div>
  )
}
const FeedbackBox = (props) => {
  const { encryptedIpAddress } = props;
  return (
    <div className="row">
      <div className="col-12">
        <div className="feedback-box p-3">
          <h5>Encrypted IP Address</h5>
          <p> {encryptedIpAddress}</p>
          <p> Note: use this Point to grant access, Save it</p>
        </div>
      </div>
    </div>
  )
}

const Divder = () => {
  return (
    <div className="row">
      <div className="col-12">
        <div className="divder ">
        </div>
      </div>
    </div>
  )
}

const GrantAccess = (props) => {
  const {grantAccess,setGrantAccess,onSumbit}= props

  const handelChange = (event) => {
    console.log(event.target.value);
    setGrantAccess(event.target.value);
  }
  return (
    <div className="row">
      <div className="col-12">
        <h3 className="mt-3">Grant Access</h3>
        <form onSubmit={onSumbit}>
          <div className="form-group">
            <label>Enter your Encrypted IP Address</label>
            <input className="input-ip" type="text" placeholder="Encrypted IP Address" onChange={handelChange}/>
            <button className="btn-encrypt" type="submit" >Grant Access</button>
          </div>
        </form>

      </div>
    </div>
  )
}




export default App;
