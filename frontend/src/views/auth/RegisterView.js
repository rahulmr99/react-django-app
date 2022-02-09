import React, { useState } from 'react';
// import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Formik } from 'formik';
import {
  Box,
  Button,
  // Checkbox,
  Container,
  FormHelperText,
  // Link,
  TextField,
  Typography,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Snackbar from '../../utils/ui/Snackbar'
import { connect } from 'react-redux';

import * as actionCreators from '../../store/actions/LoginAction';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    height: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const RegisterView = (props) => {
  const classes = useStyles();
  const navigate = useNavigate();
  let intialFormVal = {
    email: "",
    first_name:"",
    last_name:"",
    password: "",
    confirm_password: ""
  }
  const [state, setState] = useState(
    intialFormVal
)

const [reg,setReg] = useState(false);
const [errMsg,setErrMsg] = useState(false)


const handleChange = (e) => {
  const { name, value } = e.target
  setState(prevState => ({
      ...prevState,
      [name]: value
  }))
}

const handleSubmitClick = (e) => {
  e.preventDefault();

  const payload = {
      "email":state.email,
      "first_name": state.first_name, 
      "last_name": state.last_name,
      "password":state.password,
      "confirm_password":state.password
  }
  

  console.log("payload",payload)
  
  props.OnRegisterClick(payload,(res)=>{
    if(res==="success"){
      setState(intialFormVal);
      setReg(true);
      setErrMsg(null)
    }else{
      setErrMsg("Invalid Register Details")
    }
  
  })
   
}

  return (
    <Page
      className={classes.root}
      title="Register"
    >
      <Box
        display="flex"
        flexDirection="column"
        height="100%"
        justifyContent="center"
      >
        <Container maxWidth="sm">
          <Formik
            initialValues={{
              email: '',
              first_name: '',
              last_name: '',
              password: '',
              confirm_password:' ',
              policy: false
            }}
            validationSchema={
              Yup.object().shape({
                email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
                first_name: Yup.string().max(255).required('First name is required'),
                last_name: Yup.string().max(255).required('Last name is required'),
                password: Yup.string().max(255).required('password is required'),
                confirm_password: Yup.string().max(255).required('password is required'),
                policy: Yup.boolean().oneOf([true], 'This field must be checked')
              })
            }
            onSubmit={() => {
              navigate('/app/dashboard', { replace: true });
            }}
          >
            {({
              errors,
              handleBlur,
              // handleChange,
              // handleSubmit,
              isSubmitting,
              touched,
              values
            }) => (
              <form onSubmit={handleSubmitClick}>
                <Box mb={3}>
                  <Typography
                    color="textPrimary"
                    variant="h2"
                  >
                    Create new account
                  </Typography>
                  {/* <Typography
                    color="textSecondary"
                    gutterBottom
                    variant="body2"
                  >
                    Use your email to create new account
                  </Typography> */}
                </Box>
                <TextField
                  // error={Boolean(touched.first_name && errors.first_name)}
                  fullWidth
                  // helperText={touched.first_name && errors.first_name}
                  label="First name"
                  margin="normal"
                  name="first_name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  // value={(props.registerVal)?" ":(state.first_name)}
                  value={state.first_name}
                  variant="outlined"
                />
                <TextField
                  // error={Boolean(touched.last_name && errors.last_name)}
                  fullWidth
                  // helperText={touched.last_name && errors.last_name}
                  label="Last name"
                  margin="normal"
                  name="last_name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  // value={(props.registerVal)?" ":(state.last_name)}
                  value={state.last_name}
                  variant="outlined"
                />
                <TextField
                  // error={Boolean(touched.email && errors.email)}
                  fullWidth
                  // helperText={touched.email && errors.email}
                  label="Email Address"
                  margin="normal"
                  name="email"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  type="email"
                  // value={(props.registerVal)?" ":(state.email)}
                  value={state.email}
                  variant="outlined"
                />
                <TextField
                  // error={Boolean(touched.password && errors.password)}
                  fullWidth
                  // helperText={touched.password && errors.password}
                  label="Password"
                  margin="normal"
                  name="password"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  type="password"
                  value={state.password}
                  // value={(props.registerVal)?" ":(state.password)}
                  variant="outlined"
                />
                  <FormHelperText >
                   Password minimum length is 6 and should contain one uppercase letter,one lowercase letter,digit and special character 
                  </FormHelperText>
                
                 <Typography
                    color="error"
                    variant="body1"
                  >
                  {errMsg}
                    </Typography>
                {Boolean(touched.policy && errors.policy) && (
                  <FormHelperText error>
                    {errors.policy}
                  </FormHelperText>
                )}
                <Box my={2}>
                  <Button
                    color="primary"
                    disabled={isSubmitting}
                    fullWidth
                    size="large"
                    type="submit"
                    variant="contained"
                  >
                    Register 
                  </Button>
                </Box>
                <Snackbar registerSuccess={reg}/>
                
              </form>
            )}
          </Formik>
        </Container>
      </Box>
    </Page>
  );
};

const mapStateToProps = state => {
  return{
      userInfo: state.log.userInfo,
      logged: state.log.logVal,
      registerVal:state.log.registerVal

  }
}
const mapDisptachToProps = dispatch =>{
  return {
      OnRegisterClick : (payload,callback) => dispatch(actionCreators.registerCheck(payload,callback))
  }
}
export default (connect(mapStateToProps,mapDisptachToProps)(RegisterView));

