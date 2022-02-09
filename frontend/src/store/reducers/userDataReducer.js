import * as actionTypes from '../actions/userDataAction';



const intialState = {
    isLoading:true,
    addressCheck: false,
    addressListCheck :false,
    userInfo: [],
    addressList : [],
    detailedProjectInfo : [ ],
    detailedProjectCheck : false
}

const userDataReducer = (state = intialState, action) => {
    switch (action.type) {
        case actionTypes.ADDRESS_RESULT:
            console.log("userdata",action.result)
            return {
                ...state,
                userInfo: action.result,
                addressCheck: true,
                isLoading:false

            }

        case actionTypes.ADDRESS_FAILED:
            return {
                ...state,
                addressCheck: false,
                isLoading:false
            }


            case actionTypes.ADDRESS_DETAILSUCCESS:
                return {
                    ...state,
                    addressListCheck : true,
                    addressList : action.result
                }   
            case actionTypes.ADDRESS_DETAILFAILED:
                console.log("ADDRESS_DETAILFAILED",action.result)
                return {
                    ...state,
                     addressListCheck :false
                }   
            case actionTypes.DETAILPROJECT_SUCCESS:
                return {
                    ...state,
                    detailedProjectCheck : true,
                    detailedProjectInfo : action.result
                }   
            case actionTypes.DETAILPROJECT_FAILED:
                console.log("ADDRESS_DETAILFAILED",action.result)
                return {
                    ...state,
                    detailedProjectCheck :false
                }   

        default:
            return state

    }

}

export default userDataReducer;