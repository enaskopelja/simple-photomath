import React, {useState} from 'react';

import {
    Form,
    Button,
    Segment,
    Divider,
    Input,
} from "semantic-ui-react";

import {useHistory} from "react-router-dom";


export default function Upload(){
    const api = "http://127.0.0.1:5000/api/"

    const [upload, setUpload] = useState({
        name: "",
        image: null,
    })

    let history = useHistory()


    const handleImageChange = e => {
        setUpload(prevState => (
              {
                  name: e.target.files[0].name,
                  image: e.target.files[0],
              }
            )
        );
    };

    const handleSubmit = e => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('image', upload.image);
        console.log(formData.getAll('image'))


        fetch(api + 'upload', {
            method: 'POST',
            headers: {'enctype': 'multipart/form-data'},
            body: formData
        }).then(() => history.push("/solution"));
    };

      const fileInputRef = React.createRef();

      return(
           <Segment style={{ padding: "5em 1em" }} vertical>
            <Divider horizontal>UPLOAD IMAGE</Divider>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <div style ={{"display": "inline-flex"}}>
                        <Button
                            icon = 'upload'
                            label = {{ as: 'a', basic: true, content: 'Choose a file' }}
                            labelPosition = 'right'
                            onClick={() => fileInputRef.current.click()}
                            style ={{display: "inline-flex"}}
                        />
                    </div>
                    <input
                        type = "file"
                        id = "upload form"
                        ref = {fileInputRef}
                        hidden
                        onChange = {handleImageChange}
                    />

                    <Form.Input
                        labelPosition = 'left'
                        type = 'text'
                        style={{justifyContent: "center"}}
                    >
                        <Input readOnly
                               label='File chosen'
                               value={upload.name}
                               placeholder="none"
                               style={{ marginTop: "20px", width: "50%"}}/>
                    </Form.Input>

                    <Button onClick={handleSubmit} positive style={{ marginTop: "20px" }}>Upload</Button>
                </Form.Field>
                </Form>
          </Segment>

      );
}


