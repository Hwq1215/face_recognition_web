import fetch from "./fetch"

export const getFacesData = data => fetch('/manage/get',data ,'GET');

export const getFacesTotal = () => fetch('/manage/total');

// export const addFaceData = data => fetch('/manage/addFaceData', data, 'POST');

export const deleteFaceData = data => fetch('/manage/delete',data,'GET');

// export const updateFaceData = data => fetch('/manage/updateFaceData', data, 'POST');