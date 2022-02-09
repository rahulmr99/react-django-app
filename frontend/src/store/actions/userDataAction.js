import axios from 'axios';


import { API_BASE_URL } from '../../constants/apiContants';
export const ADDRESS_RESULT = 'ADDRESS_RESULT';
export const ADDRESS_FAILED = 'ADDRESS_FAILED';
export const ADDRESS_DETAILSUCCESS = 'ADDRESS_DETAILSUCCESS';
export const ADDRESS_DETAILFAILED = 'ADDRESS_DETAILFAILED';
export const FILERESULT_SUCCESS = 'FILERESULT_SUCCESS';
export const FILERESULT_FAILED = 'FILERESULT_FAILED';
export const DETAILPROJECT_SUCCESS = 'DETAILPROJECT_SUCCESS';
export const DETAILPROJECT_FAILED = 'DETAILPROJECT_FAILED';


export const addressResult = (res) => {
    console.log("inside addressRsult action")
    return {
        type: ADDRESS_RESULT,
        result: res
    };
}
export const addressFailed = (res) => {
    return {
        type: ADDRESS_FAILED,
        result: res
    };
}



export const addressCheck = (payload,callback) => {
    


    const token =localStorage.getItem('accessToken');

    const options = {
        url: API_BASE_URL + 'api/address/address/',
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': `Token ${token}`
        },
        data: payload
    };
    return dispatch => {
        axios(options)
            .then((response) => {
                console.log("resposne", response)
        
                // dispatch(addressResult)
                dispatch(addressResult(response.data))
                callback("success")

            })
            .catch(function (error) {
                dispatch(addressFailed())
                callback("failed")

            });
    }
}

export const addressDetailSuccess = (res) => {
    console.log("inside addressDetailSuccess ")
    return {
        type: ADDRESS_DETAILSUCCESS,
        result: res
    };
}
export const addressDetailFailed = (res) => {
    console.log("inside addressDetailFailed ")
    return {
        type: ADDRESS_DETAILFAILED,
        result: res
    };
}


export const addressDetails = (payload,callback) => {

    const token =localStorage.getItem('accessToken');

    const options = {
        url: API_BASE_URL + 'api/address/address/',
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': `Token ${token}`
        },
        data: payload
    };
    return dispatch => {
        // let location = useLocation();
        axios(options)
            .then((response) => {

                console.log("resp#####",response.data);
                dispatch(addressDetailSuccess(response.data))
        
                // dispatch(addressResult)
                // callback("success")

            })
            .catch(function (error) {
                console.log("error",error);
        
                dispatch(addressDetailFailed())

            });
    }
}



export const fileResult = (res) => {
    console.log("inside fileResult action")
    return {
        type: FILERESULT_SUCCESS,
        result: res
    };
}

export const fileResultFailed = (res) => {
    return {
        type: FILERESULT_FAILED,
        result: res
    };
}

export const fileCheck = (dataFile,callback) => {
   
    
    const token =localStorage.getItem('accessToken');
    console.log("file in action",dataFile)
    let bodyFormData = new FormData();
    bodyFormData.append('csv_file', dataFile);

    const options = {
        url: API_BASE_URL + 'api/address/upload-csv/',
        method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${token}`
        },
        data: bodyFormData
    };
    return dispatch => {
        axios(options)
            .then((response) => {
                console.log("resposne", response)
                // let respdata = [{"id":49,"client":"TestClient12","project_name":"Project12","address":"testaddr","building_type":null,"floors":null,"task_target":null,"consumption_overwrite":null,"utility_overwrite":null}]

                // dispatch(addressResult)
                dispatch(addressResult(response.data))
                // dispatch(addressResult(respdata))
                callback("success")
    
            })
            .catch(function (error) {
                dispatch(addressFailed())
                callback("failed")
    
            });
    }
}

export const detailedProjectSuccess = (res) => {
    console.log("inside addressDetailSuccess ")
    return {
        type: DETAILPROJECT_SUCCESS,
        result: res
    };
}
export const detailedProjectFailed = (res) => {
    console.log("inside addressDetailFailed ")
    return {
        type: DETAILPROJECT_FAILED,
        result: res
    };
}



export const detailedProject = (payload,callback) => {

    const token =localStorage.getItem('accessToken');

    const options = {
        url: API_BASE_URL + `api/address/address/${payload}`,
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': `Token ${token}`
        },
        // data: payload
    };
    return dispatch => {
        // let location = useLocation();
        axios(options)
            .then((response) => {

                console.log("resp#####",response.data);
                dispatch(detailedProjectSuccess(response.data))

            })
            .catch(function (error) {
                console.log("error",error);
        
                dispatch(detailedProjectFailed())

            });
    }
}