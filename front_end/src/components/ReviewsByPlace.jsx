import React, { useEffect, useState } from "react";
import {
    Box,
    Typography,
    Card,
    CardContent,
    Avatar,
    Divider,
    Button,
} from "@mui/material";
import Star from "@mui/icons-material/Star";

const PlaceReviews = ({ placeId, slug }) => {
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/review/reviews/by-place/${placeId}/`
                );
                const data = await response.json();
                setReviews(data);
            } catch (error) {
                console.error("Error fetching reviews:", error);
            }
        };

        fetchReviews();
    }, [placeId]);

    return (
        <Box mt={4}>
            {reviews.map((review) => (
                <Card key={review.id} sx={{ mb: 2, p: 2 }}>
                    <CardContent>
                        {/* Отображение пользователя */}
                        <Box display="flex" alignItems="center" mb={2}>
                            <Avatar
                                src={review.user_avatar || "/static/images/default_avatar.png"}
                                alt={review.user_fio}
                                sx={{ width: 50, height: 50, mr: 2 }}
                            />
                            <Typography variant="body2" fontWeight="bold">
                                {review.user_fio}
                            </Typography>
                        </Box>

                        <Divider sx={{ mb: 2 }} />

                        {/* Оценки */}
                        <Box
                            display="flex"
                            justifyContent="space-between" // Равномерное распределение оценок
                            mb={2}
                        >
                            {[
                                { label: "Цена", value: review.price },
                                { label: "Сервис", value: review.service },
                                { label: "Интерьер", value: review.interior },
                            ].map((item) => (
                                <Box
                                    key={item.label}
                                    display="flex"
                                    alignItems="center"
                                    gap={1}
                                >
                                    <Typography
                                        variant="body2"
                                        sx={{ fontWeight: "bold", whiteSpace: "nowrap" }}
                                    >
                                        {item.label}:
                                    </Typography>
                                    {[...Array(5)].map((_, index) => (
                                        <Star
                                            key={index}
                                            sx={{
                                                color: index < item.value ? "gold" : "grey.300",
                                                fontSize: 20,
                                            }}
                                        />
                                    ))}
                                </Box>
                            ))}
                        </Box>

                        <Divider sx={{ mb: 2 }} />

                        {/* Текст отзыва */}
                        <Typography variant="body1" gutterBottom>
                            {review.text}
                        </Typography>

                        {/* Дата создания */}
                        <Typography
                            variant="caption"
                            color="textSecondary"
                            display="block"
                            mt={2}
                        >
                            {new Date(review.created_at).toLocaleDateString()}
                        </Typography>
                    </CardContent>
                </Card>
            ))}
        </Box>
    );
};

export default PlaceReviews;
