import React from 'react'
import {
  Button,
  Divider,
  Grid,
  Header,
  Icon,
  Segment,
} from 'semantic-ui-react'


import {Link} from "react-router-dom";

import Upload from "./Upload";

export default function Front(){
  return(
      <Segment style = {{marginTop: "5em"}}>
          <Grid columns={2} stackable textAlign='center' style = {{backgroundColor: '#F8F8F8'}}>
              <Divider vertical>Or</Divider>

              <Grid.Row verticalAlign='middle'>
                  <Grid.Column stretched>
                      <Upload/>
                  </Grid.Column>

                  <Grid.Column stretched>
                      <Header icon>
                        <Icon name='camera'/>
                      </Header>

                      <Link to="/webcam"><Button content="Take a photo" positive/></Link>
                  </Grid.Column>

              </Grid.Row>
          </Grid>
      </Segment>
  )
  }

