export const setTokens = (accessToken, refreshToken, user_id) => {
    localStorage.setItem("access", accessToken);
    localStorage.setItem("refresh", refreshToken);
    if (user_id) {
        localStorage.setItem("user_id", user_id);
    }
};

export const getAccessToken = () => localStorage.getItem("access");

export const removeTokens = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

};
