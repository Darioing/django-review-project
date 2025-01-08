import React, { useState, useEffect } from "react";
import {
    Box,
    Button,
    TextField,
    Typography,
    Rating,
} from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const AddReviewForm = () => {
    const { slug } = useParams(); // Получение slug из URL
    const navigate = useNavigate(); // Для перенаправления
    const [place, setPlace] = useState(null); // Данные о заведении
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Поля формы
    const [priceRating, setPriceRating] = useState(0);
    const [serviceRating, setServiceRating] = useState(0);
    const [interiorRating, setInteriorRating] = useState(0);
    const [reviewText, setReviewText] = useState("");

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

    // Отправка отзыва
    const handleSubmit = async () => {
        try {
            await axios.post(
                "http://127.0.0.1:8000/review/reviews/",
                {
                    place_id: place.id,
                    user_id: localStorage.getItem("user_id"),
                    text: reviewText,
                    price: priceRating,
                    service: serviceRating,
                    interior: interiorRating,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access")}`,
                    },
                }
            );

            alert("Отзыв успешно добавлен!");
            navigate(`/place/${place.slug}`); // Перенаправление обратно к заведению
        } catch (error) {
            console.error("Ошибка при добавлении отзыва:", error);
            alert("Не удалось добавить отзыв. Попробуйте снова.");
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
                    Добавление отзыва для: {place.name}
                </Typography>

                <Typography variant="body1" align="center" gutterBottom>
                    Оцените цену:
                </Typography>
                <Rating
                    value={priceRating}
                    onChange={(event, newValue) => setPriceRating(newValue)}
                    precision={1}
                    size="large"
                    sx={{ marginBottom: "16px" }}
                />

                <Typography variant="body1" align="center" gutterBottom>
                    Оцените обслуживание:
                </Typography>
                <Rating
                    value={serviceRating}
                    onChange={(event, newValue) => setServiceRating(newValue)}
                    precision={1}
                    size="large"
                    sx={{ marginBottom: "16px" }}
                />

                <Typography variant="body1" align="center" gutterBottom>
                    Оцените интерьер:
                </Typography>
                <Rating
                    value={interiorRating}
                    onChange={(event, newValue) => setInteriorRating(newValue)}
                    precision={1}
                    size="large"
                    sx={{ marginBottom: "16px" }}
                />

                <TextField
                    fullWidth
                    label="Ваш отзыв"
                    multiline
                    rows={4}
                    variant="outlined"
                    value={reviewText}
                    onChange={(e) => setReviewText(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />

                <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                >
                    Отправить отзыв
                </Button>
            </Box>
        </Box>
    );
};

export default AddReviewForm;
