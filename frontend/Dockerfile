  
FROM node:13.12.0-alpine

# set working directory
WORKDIR /usr/src/frontend

# add `/usr/src/frontend/node_modules/.bin` to $PATH
ENV PATH /usr/src/frontend/.bin:$PATH

# install app dependencies
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install

# add app
COPY frontend/ ./

# start app
CMD ["npm", "start"]