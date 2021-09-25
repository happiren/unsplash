/*
 Navicat Premium Data Transfer

 Source Server         : happiren.com
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : localhost:3306
 Source Schema         : wallpaper

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : 65001

*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for usplash_pic
-- ----------------------------
DROP TABLE IF EXISTS `usplash_pic`;
CREATE TABLE `usplash_pic`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `pic_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '图片ID',
  `url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '原图地址',
  `width` int(10) NOT NULL DEFAULT 0 COMMENT '宽度',
  `height` int(10) NOT NULL DEFAULT 0 COMMENT '高度',
  `color` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '颜色',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '描述',
  `alt_description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'alt描述',
  `status` int(10) NOT NULL DEFAULT 0 COMMENT '状态，0:初始化 1:下载中 2:下载完成',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL COMMENT '原始json内容',
  `promoted_at` timestamp(0) NULL DEFAULT NULL COMMENT '推荐时间',
  `created_at` timestamp(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` timestamp(0) NULL DEFAULT NULL COMMENT '更新时间',
  `deleted_at` timestamp(0) NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `pic_id`(`pic_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8306 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'usplash单张图片数据' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for usplash_wallpapers
-- ----------------------------
DROP TABLE IF EXISTS `usplash_wallpapers`;
CREATE TABLE `usplash_wallpapers`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `type` int(20) NOT NULL DEFAULT 0 COMMENT '类型 1:壁纸',
  `url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '请求URL',
  `page` int(20) NOT NULL DEFAULT 0 COMMENT '分页',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL COMMENT '内容',
  `created_at` timestamp(0) NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` timestamp(0) NULL DEFAULT NULL COMMENT '更新时间',
  `deleted_at` timestamp(0) NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `type$page`(`type`, `page`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 932 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'usplash壁纸翻页爬取数据' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
