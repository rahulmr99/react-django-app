import * as actionTypes from '../actions/LoginAction';

const intialState = {
    logVal: false,
    userDetails: [],
    loginDetails: [],
    logErrMsg: null,
    regErrMsg:null,
    registerVal: false,
    headLogVal: true
}

const LoginReducer = (state = intialState, action) => {
    switch (action.type) {
        case actionTypes.LOGIN_RESULT:
            return {
                ...state,
                loginDetails: action.result,
                logVal: true,
                logErrMsg: null,

            }

        case actionTypes.REGISTER_RESULT:
            return {
                ...state,
                userDetails: action.result,
                logVal: true,
                regErrMsg: null,
                registerVal:true


            }

        case actionTypes.LOGIN_FAILED:
            return {
                ...state,
                logVal: false,
                logErrMsg: "Invalid Login details",
            }

        case actionTypes.REGISTER_FAILED:
            return {
                ...state,
                logVal: false,
                regErrMsg: "Invalid Register details",
                registerVal:false
            }
       
        case actionTypes.LOGOUT_FLAG:
            return {
                ...state,
                headLogVal: false,
                logVal: action.result
            }

        default:
            return state

    }

}

export default LoginReducer;