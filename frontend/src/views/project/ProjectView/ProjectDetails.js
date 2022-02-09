import React, { useState } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
// import { Link as RouterLink } from 'react-router-dom';

import * as actionCreators from '../../../store/actions/userDataAction';
import {
  Box,
  Button,
  Container,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  TextField,
  makeStyles,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  // Link
} from '@material-ui/core';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';

import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
// import { FileText } from 'react-feather';



const useStyles = makeStyles(() => ({
  root: {},
  table: {
    minWidth: 650,
  },
}));

const ProjectDetails = (props, { className, ...rest }) => {
  const classes = useStyles();
  let userVal = parseInt(localStorage.getItem("userId"));
  const [values, setValues] = useState({
    address: '',
    project_name: '',
    client: '',
    building_type: null,
    task_target: null,
    floors: null,
    consumption_overwrite: null,
    utility_overwrite: null,
    isAddress: false,
    rows: [],
    user: userVal,
    payload: null,
  });

  const[file,setFile] = useState(null)


  const [errMsg, setErrMsg] = useState(null)
  const [errFile, setErrFile] = useState(null)
  const [isFile,setIsFile] = useState(false)

  const handleChange = (event) => {
    setValues({
      ...values,
      [event.target.name]: event.target.value
    });

  };


  const rowAddition = () => {
    let newRow = {
      "address": values.address,
      "project_name": values.project_name,
      "client": values.client,
      "building_type": values.building_type,
      "task_target": values.task_target,
      "floors": values.floors,
      "consumption_overwrite": values.consumption_overwrite,
       "utility_overwrite":values.utility_overwrite
    }
    console.log("new Row",newRow)
    return newRow
  }
  const handleAdd = (e) => {
    e.preventDefault()
   

    if (values.client.length && values.address.length && values.project_name.length) {
      rowAddition();
      console.log("Handle add non empty values")
      setValues({
        ...values,
        rows: values.rows.concat(rowAddition()),
        address: '',
        project_name: '',
        client: '',
        building_type:  ' ',
        task_target: ' ',
        floors: ' ',
        consumption_overwrite: ' ',
        utility_overwrite: ' ',
      });
      setErrMsg(null)
    } else {
      setErrMsg("Invalid Details")
    }
  }


  const handleSave = (event) => {

    event.preventDefault();

    let apiBody = values.rows;

    if ( (values.client && values.address && values.project_name)) {
      apiBody = apiBody.concat(rowAddition())
      console.log("Row Addition happens apiBody",apiBody)

      props.OnAddressSubmit(apiBody, (res) => {
        if (res === "success") {
          setValues({
            ...values,
            isAddress: true,
            rows: [],
            address: ' ',
            project_name: ' ',
            client: ' ', 
            building_type: ' ',
            task_target: ' ',
            floors: ' ',
            consumption_overwrite: ' ',
            utility_overwrite: ' ',
          });
          setErrMsg(null)
        } else {
          setErrMsg("Please input valid details")
        }
      })
    } else{
      setErrMsg("Please input valid details")
    }
  }

  const handleFileSave = (e) =>{
    e.preventDefault()
    if(file === null || !isFile){
      console.log("file inside",file);
      setErrFile("Invalid File Input")

     
    }else{

      if(isFile) {

        props.onFileSubmit(file,(res) =>{
          console.log("res file",res);
  
          if(res==="success"){
            setValues({
              ...values,
              isAddress: true,
            });
            console.log("values address success",values.isAddress) 
            setErrFile(null) 

          }else{
            setErrFile("Invalid File Input") 
            setValues({
              ...values,
              isAddress: false,
            }) 
            console.log("values address failed",values.isAddress) 
          }
        })
      }

    }
  }


  const onChangeFile = (e) => {
    // console.log(e.target.files[0]);
    if(e.target.files[0]){
      setFile(e.target.files[0])
      setErrFile(null)
      setIsFile(true)
      
    }else{
      setIsFile(false)

    }
  }
  


  return (
    <>
      <Container maxWidth="lg">
        <Grid
          container
          spacing={2}
        >
          <Grid item xs={12}>
          <Card>
              <CardHeader
                subheader="Please add Project using File Upload or Form Input"
                title="Select an Add Project Option"
              />
              </Card>
          </Grid>
          <Grid
            item
            lg={4}
            md={6}
            xs={12}
          >
            <Card>
              <CardHeader
                // subheader=""
                title=" File Upload"
              />
              <Divider />
              <CardContent>
                <Grid
                  container
                  spacing={1}
                >
                  <Grid
                    item
                    lg={12}
                    md={12}
                    xs={12}
                  >
        <form
              autoComplete="off"
              noValidate
              className={clsx(classes.root, className)}
              {...rest}
            >                   <Typography
                      color="textPrimary"
                      variant="h6"
                    >
                      <label >Please choose your csv file </label>
                    </Typography>
                    <Typography
                      color="textPrimary"
                      variant="h4"
                      p={3}
                    >
                     <br/>
                      <input type="file"  accept=".csv"  onChange={onChangeFile} />
                    
                    </Typography>
                    <br/>
                    <Divider />
                    <Typography
                  color="error"
                  variant="body1"
                >
                  <span style={{ paddingLeft: "5px" }}>{errFile}</span>
                </Typography>
                    <Box
                display="flex"
                // justifyContent="space-between"
                justifyContent="flex-end"
                p={1}
              >
                                

                <Button
                  color="primary"
                  variant="contained"
                  type="submit"
                  onClick={handleFileSave}
                >
                  Upload File
                  </Button>
              </Box>
          </form>

                  </Grid>

                </Grid>
              </CardContent>

           
            </Card>

          </Grid>
          <Grid
            item
            lg={8}
            md={6}
            xs={12}
          >

            <form
              autoComplete="off"
              noValidate
              className={clsx(classes.root, className)}
              {...rest}
            >
              <Card>
                <CardHeader
                  // subheader="Please input details using Form Fields"
                  title="Form Input"
                />
                <Divider />

                <CardContent>
                  <Grid
                    container
                    spacing={1}
                  >
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <TextField
                        fullWidth
                        label="Client name"
                        name="client"
                        onChange={handleChange}
                        value={values.client}
                        variant="outlined"
                        required
                      />
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <TextField
                        fullWidth
                        label="Project name"
                        name="project_name"
                        onChange={handleChange}
                        value={values.project_name}
                        variant="outlined"
                        required
                      />
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <FormControl variant="outlined" fullWidth >
                        <InputLabel htmlFor="outlined-age-native-simple">Building Type</InputLabel>
                        <Select
                          labelId="demo-simple-select-outlined-label"
                          id="demo-simple-select-outlined"
                          value={values.building_type}
                          name="building_type"
                          onChange={handleChange}
                          label="buildingType"
                        >
                          <MenuItem value = { null}>
                            <em>None</em>
                          </MenuItem>
                          <MenuItem value={'OMU'}>Office Mixed Building</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <FormControl variant="outlined" fullWidth>
                        <InputLabel htmlFor="outlined-age-native-simple">Task Target</InputLabel>
                        <Select
                          labelId="demo-simple-select-outlined-label"
                          id="demo-simple-select-outlined"
                          value={values.task_target}
                          name="task_target"
                          onChange={handleChange}
                          label="Task Target"
                        >
                          <MenuItem value= { null}>
                            <em>None</em>
                          </MenuItem>
                          <MenuItem value={'CO'}>Consumption Offset</MenuItem>
                          <MenuItem value={'MS'}>Max Size</MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <TextField
                        fullWidth
                        label="Number of Floors"
                        name="floors"
                        onChange={handleChange}
                        value={values.floors}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                      <TextField
                        fullWidth
                        label="Consumption Overwrite"
                        name="consumption_overwrite"
                        onChange={handleChange}
                        value={values.consumption_overwrite}
                        variant="outlined"
                      />
                    </Grid>
                    <Grid
                      item
                      md={6}
                      xs={12}
                    >
                       <TextField
                        fullWidth
                        label="Utility Rate Overwrite"
                        name="utility_overwrite"
                        onChange={handleChange}
                        value={values.utility_overwrite}
                        variant="outlined"
                      />
                      
                    </Grid>

                    <Grid
                      item
                      md={12}
                      xs={12}
                    >
                      <TextField
                        multiline
                        rows={3}
                        rowsMax={15}
                        placeholder="Address"
                        fullWidth
                        label="Address"
                        name="address"
                        onChange={handleChange}
                        required
                        value={values.address}
                        variant="outlined"
                      />
                    </Grid>
                  </Grid>
                </CardContent>
                <Divider />

                <Typography
                  color="error"
                  variant="body1"
                >

                  <span style={{ paddingLeft: "15px" }}>{errMsg}</span>
                </Typography>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  p={1}
                >
                  <Button
                    // color="secondary"
                    variant="contained"
                    onClick={handleAdd}
                  >
                    <span style={{ color: "blue" }}>Add Another</span>
                  </Button>
                  <Button
                    color="primary"
                    variant="contained"
                    type="submit"
                    onClick={handleSave}
                  >
                    Save details
               </Button>
                </Box>
              </Card>
            </form>

          </Grid>
        </Grid>
      </Container>
      <br></br>
      {values.isAddress ?
        <Card>
          <CardHeader
            title="Added Projects"
          />
          <Divider />

          <CardContent>
            <TableContainer component={Paper}>
              <Table className={classes.table} size="small" aria-label="a dense table">
                <TableHead>
                  <TableRow>
                  <TableCell>Client Name</TableCell>
                <TableCell>Project</TableCell>
                <TableCell>Address </TableCell>
                <TableCell>Building Type </TableCell>
                <TableCell>Number of Floors </TableCell>
                <TableCell> Task Target</TableCell>
                <TableCell> Consumption Overwrite</TableCell>
                <TableCell>Utility Overwrite</TableCell>
                {/* <TableCell> Image url</TableCell> */}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {props.userInfo.map((row) => (
                    <TableRow key={row.projectName}>
                      <TableCell >{row.client}</TableCell>
                      <TableCell >{row.project_name}</TableCell>
                      <TableCell >{row.address}</TableCell>
                      <TableCell >{row.building_type}</TableCell>
                      <TableCell >{row.floors}</TableCell>
                      <TableCell >{row.task_target}</TableCell>
                      <TableCell >{row.consumption_overwrite}</TableCell>
                      <TableCell >{row.utility_overwrite}</TableCell>
                      <TableCell >
                        {/* <Button
                          variant="outlined" color="primary" size="small"
                          onClick={
                            <Link
                              component={RouterLink}
                              to="/app/dashboard"
                              variant="h5"
                            >
                            </Link>
                          }
                        >
                          <span style={{ textTransform: "lowercase" }}> Details</span>
                        </Button> */}
                         {/* img/rooftop/detail */}
                      </TableCell>
                      {/* <TableCell align="right"></TableCell> */}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
        : null
      }
    </>
  );
};


const mapStateToProps = state => {
  console.log("state in  profile details", state)
  return {
    userInfo: state.user.userInfo,
    loginInfo: state.log.loginDetails
  }
}
const mapDisptachToProps = dispatch => {
  return {
    OnAddressSubmit: (payload, callback) => dispatch(actionCreators.addressCheck(payload, callback)),
    onFileSubmit: (dataFile,callback) => dispatch(actionCreators.fileCheck(dataFile, callback))
  }
}
export default (connect(mapStateToProps, mapDisptachToProps)(ProjectDetails));
