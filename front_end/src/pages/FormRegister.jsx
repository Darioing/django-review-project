import React, { useState, useContext } from "react";
import axios from "axios";
import {
    Box,
    Button,
    Checkbox,
    FormControlLabel,
    TextField,
    Typography,
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import { AuthContext } from "../contexts/AuthContext"; // Импорт контекста авторизации
import { setTokens } from "../utils/auth"; // Утилиты для токенов
import { useNavigate } from "react-router-dom"; // Импорт useNavigate

const FormRegister = () => {
    const [FIO, setFIO] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [agreement, setAgreement] = useState(false);
    const { setIsAuthenticated } = useContext(AuthContext); // Получение функции изменения статуса авторизации
    const navigate = useNavigate(); // Инициализация навигации

    const handleSubmit = async () => {
        if (!agreement) {
            alert("Вы должны согласиться с условиями!");
            return;
        }

        try {
            // Регистрация пользователя
            const registerResponse = await axios.post("http://127.0.0.1:8000/user/register/", {
                FIO,
                email,
                password,
            });

            alert("Регистрация успешна!");
            console.log(registerResponse.data);

            // Автоматический вход после успешной регистрации
            const loginResponse = await axios.post("http://127.0.0.1:8000/user/login/", {
                email,
                password,
            });

            // Сохранение токенов
            const { access, refresh, user_id } = loginResponse.data;
            setTokens(access, refresh, user_id);

            // Установка статуса авторизации
            setIsAuthenticated(true);

            alert("Вход выполнен успешно!");
            console.log(loginResponse.data);

            navigate("/");  // Перенаправление на главную страницу
        } catch (error) {
            console.error(error);
            alert("Ошибка регистрации или авторизации.");
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
                    Регистрация
                </Typography>

                <TextField
                    fullWidth
                    label="ФИО"
                    type="text"
                    variant="outlined"
                    value={FIO}
                    onChange={(e) => setFIO(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />
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

                <FormControlLabel
                    control={
                        <Checkbox
                            checked={agreement}
                            onChange={(e) => setAgreement(e.target.checked)}
                            icon={
                                <Box
                                    sx={{
                                        width: "24px",
                                        height: "24px",
                                        border: "2px solid black",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <CheckIcon sx={{ color: "black", fontSize: "16px" }} />
                                </Box>
                            }
                            checkedIcon={
                                <Box
                                    sx={{
                                        width: "24px",
                                        height: "24px",
                                        border: "2px solid black",
                                        backgroundColor: "lightgreen",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <CheckIcon sx={{ color: "black", fontSize: "16px" }} />
                                </Box>
                            }
                        />
                    }
                    label="Я соглашаюсь на обработку пользовательских данных"
                    sx={{ marginBottom: "16px" }}
                />

                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    sx={{ marginTop: "8px" }}
                >
                    Зарегистрироваться
                </Button>
            </Box>
        </Box>
    );
};

export default FormRegister;
