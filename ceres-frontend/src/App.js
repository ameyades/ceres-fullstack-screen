import logo from './logo.svg'
import './App.css'
import React, { useState, setState } from "react"
import axios from "axios"

function App() {
  /* state of app can be found here */
  const [image_list, updateImageList] = useState([]) //image_list is array of file names
  const [metadata, updateMetadata] = useState("Metadata will show up here!")    
  const [begin_ms, updateBeginMS] = useState(0)
  const [end_ms, updateEndMS] = useState(0)
  /* translate list of images into menu */
  const image_listing = (image_list).map(function (value) {
    return (
      <tr>
        <td> {value} </td> 
        <td> 
          <button onClick={() => 
            axios.post('/api/public/downloadImage', {'file_name': value}).then((res) => {
              console.log(res['data']['img_url'])
              const url = res['data']['img_url'] 
              const link = document.createElement('a')
              link.href = url
              link.setAttribute('download', value) 
              document.body.appendChild(link)
              link.click()
            })
          }> Download Image </button>
        </td> 
        <td> 
          <button onClick={() =>
            axios.post('/api/public/getMetadataOfImage', {'file_name': value}).then((res) => {
              updateMetadata((metadata) => res['data']['metadata'])
            }) 
          }> Get Metadata </button> 
        </td>
      </tr>
    )
  })
  /* this is a hack - directly call a get to the backend to avoid any piping issues with the JS frontend when downloading the zip */
  const downloadFile = () => {
    window.location.href = "http://localhost:3334/api/public/getZipOfAllImages"
  }
  /* main view */
  return (
    <div>
      <h1> Ceres Image Getter </h1> 
      <div>
        <div>
          <button onClick={() => {
            axios.post('/api/public/getListOfImages').then((res) => {
              console.log(res['data']['list'])
              updateImageList((image_list) => [...res['data']['list']])
            })
          }}> Get Image Listing </button>
        </div>
        <div style={{display: 'flex'}}>
          <button onClick={() => {
            axios.post('/api/public/getListOfImagesInTime', {'begin_time': begin_ms, 'end_time': end_ms}).then((res) => {
              console.log(res)
              updateImageList((image_list) => [...res['data']['img_list']])
            })
          }}> Get Image Listing Within Corresponding Times </button>
          <div style={{'padding-left': '5px'}}>  Begin time in Milliseconds (after 2020-06-01 17:41:07): <input type="number" onChange={(event) => {updateBeginMS(event.target.value)}} value={begin_ms} /> </div>
          <div style={{'padding-left': '5px'}}> End time in Milliseconds: <input type="number" onChange={(event) => {updateEndMS(event.target.value)}} value={end_ms} /> </div>
        </div>
        <button type="submit" onClick={downloadFile}>Download Zip File</button>
        <h2> Image Listing </h2>
        <table>{image_listing}</table>
        <div>
          <h2> Selected Metadata </h2>
          {metadata}
        </div>
      </div>
    </div>
  )
}

export default App
