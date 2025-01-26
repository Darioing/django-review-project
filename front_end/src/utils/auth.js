export const setTokens = (accessToken, refreshToken, user_id) => {
    removeTokens();
    localStorage.setItem("access", accessToken);
    localStorage.setItem("refresh", refreshToken);
    localStorage.setItem("user_id", user_id);
};

export const getAccessToken = () => localStorage.getItem("access");

export const removeTokens = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user_id");
};
