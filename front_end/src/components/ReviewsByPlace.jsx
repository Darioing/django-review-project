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
import CommentThread from "./CommentThread";
import AddCommentForm from "./AddCommentForm";
import VoteControl from "./VoteControl";

const PlaceReviews = ({ placeId }) => {
    const [reviews, setReviews] = useState([]);
    const [comments, setComments] = useState({});
    const [activeReviewId, setActiveReviewId] = useState(null);
    const [replyTarget, setReplyTarget] = useState(null); // Объект, к которому добавляется комментарий

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

    const fetchComments = async (reviewId) => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/review/comments/${reviewId}/by-object/?content_type=13`
            );
            const data = await response.json();
            setComments((prev) => ({ ...prev, [reviewId]: data }));
        } catch (error) {
            console.error("Ошибка при загрузке комментариев:", error);
        }
    };


    const handleAddComment = async (targetObject, commentText) => {
        const data = {
            user_id: localStorage.getItem("user_id"),
            content_type: targetObject.self_content_type,
            object_id: targetObject.id,
            text: commentText,
        };

        try {
            const response = await fetch(`http://127.0.0.1:8000/review/comments/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access")}`,
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const newComment = await response.json();
                console.log("Добавлен новый комментарий:", newComment);

                setComments((prev) => {
                    const updatedComments = { ...prev };

                    // Добавляем комментарий в правильное место
                    if (targetObject.self_content_type === 13) {
                        // Добавление на корневой уровень
                        updatedComments[targetObject.id] = [
                            ...(updatedComments[targetObject.id] || []),
                            newComment,
                        ];
                    } else {
                        // Добавление в ветвь комментариев
                        const updateBranch = (comments) => {
                            return comments.map((comment) => {
                                if (comment.id === targetObject.id) {
                                    return {
                                        ...comment,
                                        children: [...(comment.children || []), newComment],
                                    };
                                } else if (comment.children && comment.children.length > 0) {
                                    return {
                                        ...comment,
                                        children: updateBranch(comment.children),
                                    };
                                }
                                return comment;
                            });
                        };

                        updatedComments[targetObject.object_id] = updateBranch(
                            updatedComments[targetObject.object_id] || []
                        );
                    }

                    console.log("Обновлённые комментарии:", updatedComments);
                    return updatedComments;
                });

                // Автоматическое открытие ветви
                setActiveReviewId((prev) => (prev === targetObject.object_id ? prev : targetObject.object_id));
                setReplyTarget(null); // Закрываем форму добавления комментария
            } else {
                console.error("Ошибка при добавлении комментария:", await response.text());
            }
        } catch (error) {
            console.error("Ошибка при отправке комментария:", error);
        }
    };
    const handleToggleComments = (reviewId) => {
        if (!comments[reviewId]) {
            fetchComments(reviewId); // Если комментарии ещё не загружены, подгружаем их
        }
        setActiveReviewId((prev) => (prev === reviewId ? null : reviewId)); // Переключаем видимость
    };


    return (
        <Box mt={4}>
            {reviews.map((review) => (
                <Card key={review.id} sx={{ mb: 2, p: 2, display: "flex", alignItems: "flex-start" }}>
                    {/* Компонент с голосованием и отзывом */}
                    <Box display="flex" flexDirection="row" flex={1}>
                        {/* Блок голосования */}
                        <Box
                            display="flex"
                            flexDirection="column"
                            alignItems="center"
                            justifyContent="flex-start"
                            sx={{ mr: 2, minWidth: 50 }}
                        >
                            <VoteControl
                                contentType={review.self_content_type}
                                objectId={review.id}
                                onVote={(vote) => console.log("New vote:", vote)}
                            />
                        </Box>

                        {/* Основной блок отзыва */}
                        <Box flex={1}>
                            <CardContent sx={{ p: 0 }}>
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

                                {/* Оценки */}
                                <Box display="flex" justifyContent="space-between" mb={2}>
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

                                {/* Кнопки */}
                                <Box mt={2}>
                                    <Button
                                        variant="text"
                                        color="primary"
                                        sx={{
                                            mr: 2,
                                            display: review.comment_count > 0 ? "inline-flex" : "none"
                                        }}
                                        onClick={() => {
                                            setActiveReviewId(activeReviewId === review.id ? null : review.id);
                                            fetchComments(review.id);
                                        }}
                                    >
                                        {activeReviewId === review.id ? "Скрыть комментарии" : "Показать комментарии"}
                                    </Button>
                                    <Button
                                        variant="text"
                                        color="primary"
                                        onClick={() =>
                                            setReplyTarget(
                                                replyTarget?.id === review.id &&
                                                    replyTarget?.self_content_type === review.self_content_type
                                                    ? null // Скрываем форму, если она уже открыта для этого отзыва
                                                    : review // Устанавливаем target, если форма ещё не открыта
                                            )
                                        }
                                    >
                                        {replyTarget?.id === review.id ? "Отменить" : "Ответить"}
                                    </Button>
                                </Box>
                            </CardContent>

                            {/* Форма добавления комментария */}
                            {replyTarget &&
                                replyTarget.id === review.id &&
                                replyTarget.self_content_type === review.self_content_type && (
                                    <AddCommentForm
                                        onSubmit={(target, text) => handleAddComment(target, text)}
                                        targetObject={replyTarget}
                                        onCancel={() => setReplyTarget(null)}
                                    />
                                )}

                            {/* Отображение комментариев */}
                            {activeReviewId === review.id && (
                                <Box mt={2}>
                                    <CommentThread
                                        comments={comments[review.id] || []}
                                        onReply={(comment) => setReplyTarget(comment)}
                                        replyTarget={replyTarget}
                                        onCancelReply={() => setReplyTarget(null)}
                                        onAddComment={(target, text) =>
                                            handleAddComment(target, text)
                                        }
                                        key={review.id + JSON.stringify(comments[review.id] || [])}
                                    />
                                </Box>
                            )}
                        </Box>
                    </Box>
                </Card>
            ))}
        </Box>



    );
};

export default PlaceReviews;
