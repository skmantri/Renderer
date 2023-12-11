import numpy as np
from transform import Transform
class OrthoCamera:
    def __init__(self, left, right, top, bottom, near, far):
        self.transform = Transform()
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far

        rml = self.right - self.left
        tmb = self.top - self.bottom
        fmn = self.far - self.near

        self.orthographic_transform = np.array([
            [2 / rml, 0, 0, -((self.right + self.left) / rml)],
            [0, 2 / fmn, 0, -((self.far + self.near) / fmn)],
            [0, 0, -2 / tmb, -((self.top + self.bottom) / tmb)],
            [0, 0, 0, 1]
        ])

    def ratio(self):
        width = self.right - self.left
        height = self.top - self.bottom

        return abs(width/height)

    def project_point(self, p):
        # transform p from world to camera space
        p_camera = self.transform.apply_inverse_to_point(p)

        # transform p_camera from camera to screen space
        p_camera = np.append(p_camera, 1.0)
        p_screen = np.matmul(self.orthographic_transform, p_camera)
        return p_screen[:3]
class PerspectiveCamera:
    def __init__(self, left, right, top, bottom, near, far):
        self.transform = Transform()
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far

        self.orthographic_transform = np.array([
            [2 / (self.right - self.left), 0, 0, -((self.right + self.left) / (self.right - self.left))],
            [0, 2 / (self.far - self.near), 0, -((self.far + self.near) / (self.far - self.near))],
            [0, 0, (-2) / (self.top - self.bottom), -((self.top + self.bottom) / (self.top - self.bottom))],
            [0, 0, 0, 1]
        ])

        self.perspective_projection_matrix = np.array([
            [self.near, 0, 0, 0],
            [0, self.near + self.far, 0, -1 * self.far * self.near],
            [0, 0, self.near, 0],
            [0, 1, 0, 0]
        ])

        self.inverse_perspective_projection_matrix = np.array([
            [1 / self.near, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1 / self.near, 0],
            [0, 1 / (self.near * self.far), 0, (self.near + self.far) / (self.near * self.far)]
        ])

    def ratio(self):
        width = self.right - self.left
        height = self.top - self.bottom
        return abs(width/height)

    def project_point(self, p):
        # transform p from world to camera space
        p_camera = self.transform.apply_inverse_to_point(p)
        p_camera = np.append(p_camera, 1.0)
        p_p1 = np.matmul(self.perspective_projection_matrix, p_camera)
        p_p2 = p_p1 / p_p1[3]
        p_screen = np.matmul(self.orthographic_transform, p_p2)
        return p_screen[:3]

    def project_inverse_point(self, p):
        p = np.append(p, 1)

        # create an inverse orthographic transformation matrix
        inverse_ortho = np.linalg.inv(self.orthographic_transform)
        p_p1 = np.matmul(inverse_ortho, p)
        y_c = (self.near * self.far) / ((self.near + self.far) - p_p1[1])
        p_p2 = p_p1 * y_c
        p_camera = np.matmul(self.inverse_perspective_projection_matrix, p_p2)[:3]
        p_world = self.transform.apply_to_point(p_camera)
        return p_world

c = PerspectiveCamera(left=1, right=2, bottom=3, top=4, near=5, far=6)
point = np.array([3, 3, 3])
print(c.perspective_projection_matrix)

