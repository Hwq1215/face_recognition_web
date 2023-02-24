import fetch from "./fetch"

export const getFacesData = page => fetch('/manage/getFacesData'+page ,'GET');

export const getFacesTotal = () => fetch('/manage/getFacesTotal', data, 'GET');

// export const addFaceData = data => fetch('/manage/addFaceData', data, 'POST');

export const deleteFaceData = faceId => fetch('/manage/deleteFaceData'+faceId, 'POST');

// export const updateFaceData = data => fetch('/manage/updateFaceData', data, 'POST');