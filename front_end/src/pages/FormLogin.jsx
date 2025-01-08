import React, { useState, useContext } from "react";
import axios from "axios";
import {
    Box,
    Button,
    TextField,
    Typography,
} from "@mui/material";
import { AuthContext } from "../contexts/AuthContext"; // Импорт контекста аутентификации
import { setTokens } from "../utils/auth"; // Утилиты для работы с токенами
import { useNavigate } from "react-router-dom"; // Импорт useNavigate

const FormLogin = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const { setIsAuthenticated } = useContext(AuthContext); // Доступ к функции изменения статуса авторизации
    const navigate = useNavigate(); // Инициализация навигации

    const handleSubmit = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/user/login/", {
                email,
                password,
            });

            // Сохранение токенов в локальное хранилище
            const { access, refresh, user_id } = response.data;
            setTokens(access, refresh, user_id);

            // Установка статуса авторизации
            setIsAuthenticated(true);

            alert("Вход выполнен успешно!");
            console.log(response.data);

            navigate("/"); // Перенаправление на главную страницу
        } catch (error) {
            console.error(error);
            alert("Неверный email или пароль.");
        }
    };

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "calc(100vh - 64px - 62px)",
                backgroundColor: "background.default",
                padding: "16px",
            }}
        >
            <Box
                sx={{
                    width: "100%",
                    maxWidth: "400px",
                    padding: "24px",
                    backgroundColor: "background.paper",
                    borderRadius: "8px",
                    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Typography variant="h5" align="center" gutterBottom>
                    Вход
                </Typography>

                <TextField
                    fullWidth
                    label="Email"
                    type="email"
                    variant="outlined"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />
                <TextField
                    fullWidth
                    label="Пароль"
                    type="password"
                    variant="outlined"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />

                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    sx={{ marginTop: "8px" }}
                >
                    Войти
                </Button>
            </Box>
        </Box>
    );
};

export default FormLogin;
