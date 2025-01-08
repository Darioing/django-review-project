import React, { useState, useEffect } from "react";
import {
    Box,
    Button,
    TextField,
    Typography,
} from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const AddQuestionForm = () => {
    const { slug } = useParams(); // Получение slug из URL
    const navigate = useNavigate(); // Для перенаправления
    const [place, setPlace] = useState(null); // Данные о заведении
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Поля формы
    const [questionText, setQuestionText] = useState("");

    // Загрузка данных о заведении
    useEffect(() => {
        const fetchPlace = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/review/places/${slug}/`);
                setPlace(response.data);
                setLoading(false);
            } catch (err) {
                setError("Ошибка при загрузке данных заведения");
                setLoading(false);
            }
        };

        fetchPlace();
    }, [slug]);

    // Отправка вопроса
    const handleSubmit = async () => {
        try {
            await axios.post(
                "http://127.0.0.1:8000/review/questions/",
                {
                    place_id: place.id,
                    user_id: localStorage.getItem("user_id"),
                    text: questionText,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access")}`,
                    },
                }
            );

            alert("Вопрос успешно добавлен!");
            navigate(`/place/${place.slug}`); // Перенаправление обратно к заведению
        } catch (error) {
            console.error("Ошибка при добавлении вопроса:", error);
            alert("Не удалось добавить вопрос. Попробуйте снова.");
        }
    };

    // Обработка состояния загрузки и ошибок
    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Typography variant="h6">Загрузка данных...</Typography>
            </Box>
        );
    }

    if (error) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Typography variant="h6" color="error">
                    {error}
                </Typography>
            </Box>
        );
    }

    if (!place) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Typography variant="h6" color="error">
                    Данные о заведении не найдены.
                </Typography>
            </Box>
        );
    }

    // Основной рендеринг формы
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
                    maxWidth: "500px",
                    padding: "24px",
                    backgroundColor: "background.paper",
                    borderRadius: "8px",
                    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Typography variant="h6" align="center" gutterBottom>
                    Задать вопрос для: {place.name}
                </Typography>

                <TextField
                    fullWidth
                    label="Ваш вопрос"
                    multiline
                    rows={4}
                    variant="outlined"
                    value={questionText}
                    onChange={(e) => setQuestionText(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />

                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                >
                    Отправить вопрос
                </Button>
            </Box>
        </Box>
    );
};

export default AddQuestionForm;
