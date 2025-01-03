import React, { createContext, useState, useEffect } from "react";
import { getAccessToken, removeTokens } from "../utils/auth";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Проверяем наличие токена при загрузке
        const token = getAccessToken();
        setIsAuthenticated(!!token);
    }, []);

    const logout = () => {
        removeTokens();
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
