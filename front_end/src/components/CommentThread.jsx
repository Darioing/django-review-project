import React, { useState, useEffect } from "react";
import { Box, Typography, Avatar, Divider, Button } from "@mui/material";
import AddCommentForm from "./AddCommentForm";

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
                <Box key={comment.id} ml={Math.min(level * 2, 16)} mb={2}>
                    {/* Основная информация о комментарии */}
                    <Box display="flex" alignItems="center" mb={1}>
                        <Avatar
                            src={comment.user_avatar}
                            alt={comment.user_fio}
                            sx={{ mr: 1 }}
                        />
                        <Typography variant="body2" fontWeight="bold">
                            {comment.user_fio}
                        </Typography>
                    </Box>
                    <Typography variant="body1">{comment.text}</Typography>
                    <Typography variant="caption" color="textSecondary">
                        {new Date(comment.created_at).toLocaleDateString()}
                    </Typography>

                    {/* Кнопки управления */}
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
                            color="secondary"
                            onClick={() => onReply(comment)}
                        >
                            Ответить
                        </Button>
                    </Box>

                    {replyTarget && replyTarget.id === comment.id && (
                        <AddCommentForm
                            onSubmit={(target, text) => onAddComment(target, text)}
                            targetObject={replyTarget}
                            onCancel={onCancelReply} // Кнопка отмены
                        />
                    )}

                    <Divider sx={{ mt: 1, mb: 1 }} />

                    {/* Рекурсивное отображение ветви */}
                    {isExpanded && comment.children && renderComments(comment.children, level + 1)}
                </Box>
            );
        });
    };

    return <Box>{renderComments(comments)}</Box>;
};

export default CommentThread;
