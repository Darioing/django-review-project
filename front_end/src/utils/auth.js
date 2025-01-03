export const setTokens = (accessToken, refreshToken) => {
    localStorage.setItem("access", accessToken);
    localStorage.setItem("refresh", refreshToken);
};

export const getAccessToken = () => localStorage.getItem("access");

export const removeTokens = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
};
