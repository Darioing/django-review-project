import React, { useState, useEffect } from "react";
import { Box, Typography, Avatar, Divider, Button } from "@mui/material";
import AddCommentForm from "./AddCommentForm";
import VoteControl from "./VoteControl";

const CommentThread = ({ comments, onReply, replyTarget, onCancelReply, onAddComment }) => {
    const [expandedComments, setExpandedComments] = useState([]);

    const toggleCommentBranch = (commentId) => {
        setExpandedComments((prev) =>
            prev.includes(commentId)
                ? prev.filter((id) => id !== commentId)
                : [...prev, commentId]
        );
    };
    useEffect(() => {
        // Проверяем, открыты ли ветви комментариев и повторно их открываем
        setExpandedComments((prev) => {
            const activeComments = comments.map((comment) => comment.id);
            return prev.filter((id) => activeComments.includes(id));
        });
    }, [comments]);

    const renderComments = (comments, level = 0) => {
        return comments.map((comment) => {
            const isExpanded = expandedComments.includes(comment.id);

            return (
                <Box key={comment.id} sx={{ mb: 2 }}>
                    {/* Внешний контейнер для одного уровня комментария */}
                    <Box
                        sx={{
                            display: "flex",
                            alignItems: "flex-start",
                            pl: `${level * 20}px`, // Вложенность через padding
                        }}
                    >
                        {/* Блок голосования */}
                        <Box
                            display="flex"
                            flexDirection="column"
                            alignItems="center"
                            justifyContent="flex-start"
                            sx={{ mr: 2 }}
                        >
                            <VoteControl
                                contentType={comment.self_content_type}
                                objectId={comment.id}
                                onVote={(vote) => console.log("New vote for comment:", vote)}
                            />
                        </Box>

                        {/* Основной текст комментария */}
                        <Box sx={{ flex: 1 }}>
                            {/* Информация о пользователе */}
                            <Box display="flex" alignItems="center" mb={1}>
                                <Avatar
                                    src={comment.user_avatar || "/static/images/default_avatar.png"}
                                    alt={comment.user_fio}
                                    sx={{ mr: 1, width: 30, height: 30 }}
                                />
                                <Typography variant="body2" fontWeight="bold">
                                    {comment.user_fio}
                                </Typography>
                            </Box>

                            {/* Текст комментария */}
                            <Typography variant="body1" sx={{ fontSize: 14, mb: 1 }}>
                                {comment.text}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                {new Date(comment.created_at).toLocaleDateString()}
                            </Typography>

                            {/* Управляющие кнопки */}
                            <Box mt={1}>
                                {comment.children && comment.children.length > 0 && (
                                    <Button
                                        variant="text"
                                        size="small"
                                        color="primary"
                                        onClick={() => toggleCommentBranch(comment.id)}
                                    >
                                        {isExpanded ? "Скрыть ветвь" : "Открыть ветвь"}
                                    </Button>
                                )}
                                <Button
                                    variant="text"
                                    size="small"
                                    color="primary"
                                    onClick={() => onReply(comment)}
                                >
                                    Ответить
                                </Button>
                            </Box>

                            {/* Форма добавления комментария */}
                            {replyTarget && replyTarget.id === comment.id && (
                                <AddCommentForm
                                    onSubmit={(target, text) => onAddComment(target, text)}
                                    targetObject={replyTarget}
                                    onCancel={onCancelReply}
                                />
                            )}
                        </Box>
                    </Box>

                    {/* Вложенные комментарии */}
                    {isExpanded &&
                        comment.children &&
                        comment.children.map((childComment) =>
                            renderComments([childComment], level + 1)
                        )}
                </Box>
            );
        });
    };

    return <Box>{renderComments(comments)}</Box>;
};

export default CommentThread;
