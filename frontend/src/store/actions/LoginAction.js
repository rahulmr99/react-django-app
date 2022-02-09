import axios from 'axios';

import { API_BASE_URL } from '../../constants/apiContants';
export const LOGIN_RESULT = 'LOGIN_RESULT';
export const REGISTER_RESULT = 'REGISTER_RESULT';
export const LOGIN_FAILED = 'LOGIN_FAILED';
export const REGISTER_FAILED = 'REGISTER_FAILED';
export const LOGOUT_FLAG = 'LOGOUT_FLAG';

export const loginResult = (res) => {
    return {
        type: LOGIN_RESULT,
        result: res
    };
}
export const loginFailed = (res) => {
    return {
        type: LOGIN_FAILED,
        result: res
    };
}

export const LogOutFlag = (res) => {
    return {
        type: LOGOUT_FLAG,
        result: res
    };
}

export const registerResult = (res) => {
    return {
        type: REGISTER_RESULT,
        result: res
    };
}

export const registerFailed = (res) => {
    return {
        type: REGISTER_FAILED,
        result: res
    };
}


export const loginCheck = (payload) => {
    const options = {
        url: API_BASE_URL + 'api/users/login/',
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        },
        data: payload
    };
    return dispatch => {
        axios(options)
            .then((response) => {
            
                // localStorage.setItem('accessToken', response.data.token);
                localStorage.setItem('userId', response.data.id);
                localStorage.setItem('userName', response.data.first_name);
                localStorage.setItem('userType', response.data.type);
          
                dispatch(loginResult(response.data));

            })
            .catch(function (error) {
                console.log("err", error);
                dispatch(loginFailed())
            });
    }
}


export const registerCheck = (payload,callback) => {

    const options = {
        url: API_BASE_URL + 'api/users/register/',
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        },
        data: payload
    };

    return dispatch => {
        axios(options)
            .then((response) => {
                
                console.log(response);
                dispatch(registerResult(response.data));
                callback("success")


            })
            .catch(function (error) {
                console.log("err", error);
                dispatch(registerFailed())
                callback("failed")
            });
    }

}


